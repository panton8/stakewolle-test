from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.response import Response
from core.user.serializers import (UserSerializer, ReferralCodeSerializer, AddReferralCodeSerializer, ReferralSerializer,
                                   EmailSerializer)
from core.user.models import User, ReferralCode, ReferralRelationship
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os

load_dotenv()


class UserViewSet(viewsets.ModelViewSet):
    http_method_names = ('get', 'patch')
    permission_classes = (IsAuthenticated, )
    serializer_class = UserSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()
        return User.objects.exclude(is_superuser=True)

    def get_object(self):
        obj = User.objects.get_object_by_public_id(self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)

        return obj


class ReferralCodeViewSet(viewsets.ModelViewSet):
    queryset = ReferralCode.objects.all()
    serializer_classes = {
        "create": AddReferralCodeSerializer,
        "default": ReferralCodeSerializer,
    }
    permission_classes = (IsAuthenticated, )
    http_method_names = ('get', 'post',)

    def get_queryset(self):
        if self.action == "list":
            if not self.request.user.is_superuser:
                return ReferralCode.objects.filter(creator=User.objects.get(email=self.request.user.email))
        return self.queryset

    def get_serializer_class(self):
        return self.serializer_classes.get(
            self.action, self.serializer_classes["default"]
        )


class ReferralViewSet(viewsets.ModelViewSet):
    queryset = ReferralRelationship.objects.all()
    serializer_class = ReferralSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(referrer=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        user = User.objects.get_object_by_public_id(self.kwargs['pk'])
        referrals = self.queryset.filter(referrer=user)
        serializer = self.get_serializer(referrals, many=True)
        return Response(serializer.data)


class ShareRefCodeViewSet(viewsets.ViewSet):
    serializer_class = EmailSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                msg = EmailMessage()
                msg["Subject"] = "Referral Code Sharing"
                msg["From"] = request.user.email
                msg["To"] = email
                msg.set_content(
                    f"Referral code: {request.user.referral_code.code}\n"
                    f"Valid Until: {request.user.referral_code.valid_until}\n"
                )
                with smtplib.SMTP_SSL(os.getenv("EMAIL_HOST"), os.getenv("EMAIL_PORT")) as server:
                    server.login(os.getenv("EMAIL_HOST_USER"), os.getenv("EMAIL_HOST_PASSWORD"))
                    server.send_message(msg)
                return Response({'message': 'Email sent successfully'}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)