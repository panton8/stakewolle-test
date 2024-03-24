from rest_framework import serializers

from core.user.serializers import UserSerializer
from core.user.models import User, ReferralCode, ReferralRelationship

from django.utils import timezone


class RegisterSerializer(UserSerializer):
    """
    Registration serializer for requests and user creation
    """
    password = serializers.CharField(max_length=128, min_length=8, write_only=True, required=True)
    referral_code = serializers.CharField(max_length=8, write_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'password', 'referral_code']

    def create(self, validated_data):
        referral_code = validated_data.pop('referral_code', None)

        user = User.objects.create_user(**validated_data)

        if referral_code:
            try:
                code_obj = ReferralCode.objects.get(code=referral_code)
                if code_obj.valid_until >= timezone.now():
                    referral = ReferralRelationship(referrer=code_obj.creator, referred_user=user)
                    referral.save()

                    code_obj.creator.bonus += 20
                    code_obj.creator.save()

                    user.bonus += 8
                    user.save()
                else:
                    user.delete()
                    raise serializers.ValidationError("Referral code has expired or is invalid.")
            except ReferralCode.DoesNotExist:
                raise serializers.ValidationError("Referral code not found.")

        return user

