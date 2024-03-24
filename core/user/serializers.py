from rest_framework import serializers
from core.user.models import User, ReferralCode, ReferralRelationship
from django.core.validators import MinValueValidator, MaxValueValidator
import random
import string
from django.utils import timezone


class UserSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='public_id', read_only=True, format='hex')
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name',
                  'last_name', 'email', 'is_active',
                  'created', 'updated', 'referral_code', 'bonus'
                  ]
        read_only_fields = ['is_active', 'referral_code', 'bonus']


class ReferralCodeSerializer(serializers.ModelSerializer):
    code = serializers.CharField(read_only=True)
    valid_until = serializers.DateTimeField(read_only=True)

    class Meta:
        model = ReferralCode
        fields = ['code', 'valid_until']


class AddReferralCodeSerializer(serializers.ModelSerializer):
    code = serializers.CharField(read_only=True)
    valid_until = serializers.DateTimeField(read_only=True)
    creator = serializers.CharField(read_only=True)
    valid_days = serializers.IntegerField(write_only=True, validators=[
            MinValueValidator(1, message="Value must be greater than or equal to 1"),
            MaxValueValidator(31, message="Value must be less than or equal to 31")
        ])

    class Meta:
        model = ReferralCode
        fields = ['code', 'valid_until', 'creator', 'valid_days']

    def create(self, validated_data):
        user = self.context['request'].user

        old_referral_code = user.referral_code

        if old_referral_code:
            old_referral_code.delete()

        valid_days = validated_data.pop('valid_days')
        validated_data["valid_until"] = timezone.now() + timezone.timedelta(days=valid_days)
        validated_data["code"] = self.generate_unique_referral_code()
        validated_data["creator"] = user

        new_referral_code = ReferralCode.objects.create(**validated_data)

        user.referral_code = new_referral_code
        user.save()

        return new_referral_code

    def generate_unique_referral_code(self):
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        while ReferralCode.objects.filter(code=code).exists():
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        return code


class ReferralSerializer(serializers.ModelSerializer):
    referred_user = UserSerializer(read_only=True)

    class Meta:
        model = ReferralRelationship
        fields = ['referred_user', 'created_at']
        read_only_fields = ['referrer', 'referred_user', 'created_at']


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)

