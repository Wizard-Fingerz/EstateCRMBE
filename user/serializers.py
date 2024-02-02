from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = '__all__'


class MarketerSerializer(serializers.ModelSerializer):
    is_marketer = serializers.BooleanField(required=True, write_only=True)
    username = serializers.CharField(validators=[RegexValidator(
        regex=r'^[\w.@+-/]+$',
        message="Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters.",
        code='invalid_username'
    )])

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'contact', 'is_marketer', 'profile_picture', 'cover_picture', 'password']

    def create(self, validated_data):
        is_marketer = validated_data.pop('is_marketer', False)
        user = super(MarketerSerializer, self).create(validated_data)
        user.is_marketer = is_marketer
        user.set_password(validated_data['password'])
        user.save()
        return user


class AccountantSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'is_accountant', 'profile_image']


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()


class MarketerCountSerializer(serializers.Serializer):
    count = serializers.IntegerField()