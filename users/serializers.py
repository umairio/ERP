from datetime import timedelta

from .models import Profile, User
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password2')

    def validate(self, attrs):
        password2 = attrs.pop('password2')
        if attrs['password'] != password2:
            raise serializers.ValidationError({'password': "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            **validated_data,
        )
        return user


class CreateProfileSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Profile
        fields = ['user', 'subscription_start_date', 'subscription_end_date']

    def validate_subscription_start_date(self, value):
        if value < timezone.now() - timedelta(minutes=10):
            raise serializers.ValidationError('Subscription date cannot be older than 10 minutes.')
        return value

    def validate_user(self, value):
        if Profile.objects.filter(user=value).exists():
            raise serializers.ValidationError('Profile for this user already exists.')
        return value


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, attrs):
        old_password = attrs.pop('password')
        new_password = attrs.get('new_password')
        user = self.context['request'].user
        if not user.check_password(old_password):
            raise serializers.ValidationError({'password': 'Wrong password.'})

        if self.context['request'].user.check_password(new_password):
            raise serializers.ValidationError({'new_password': 'Password must be different from your old password.'})
        return attrs
