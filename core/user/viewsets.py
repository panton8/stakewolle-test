from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.utils import timezone
from core.user.serializers import UserSerializer, ReferralCodeSerializer, AddReferralCodeSerializer
from core.user.models import User, ReferralCode
import random
import string


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