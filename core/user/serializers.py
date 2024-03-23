from rest_framework import serializers
from core.user.models import User, ReferralCode
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
        read_only_fields = ['is_active']


class ReferralCodeSerializer(serializers.ModelSerializer):
    code = serializers.CharField(read_only=True)
    valid_until = serializers.DateTimeField(read_only=True)
    creator = serializers.CharField(read_only=True, source='user')

    class Meta:
        model = ReferralCode
        fields = ['code', 'valid_until', 'creator']


class AddReferralCodeSerializer(serializers.ModelSerializer):
    code = serializers.CharField(read_only=True)
    valid_until = serializers.DateTimeField(read_only=True)
    creator = serializers.CharField(read_only=True)
    valid_days = serializers.IntegerField(write_only=True)

    class Meta:
        model = ReferralCode
        fields = ['code', 'valid_until', 'creator', 'valid_days']

    def create(self, validated_data):
        valid_days = validated_data.pop('valid_days')
        validated_data["valid_until"] = timezone.now() + timezone.timedelta(days=valid_days)
        validated_data["code"] = self.generate_unique_referral_code()
        validated_data["creator"] = self.context['request'].user
        return ReferralCode.objects.create(**validated_data)

    def generate_unique_referral_code(self):
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        while ReferralCode.objects.filter(code=code).exists():
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        return code