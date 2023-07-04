from rest_framework import generics, permissions
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Image
# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username','last_name', 'email','first_name')

 
# Update User Serializer
# class UpdateUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'last_name', 'email', 'first_name')
class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'last_name', 'email', 'first_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password is not None:
            instance.set_password(password)

        return super().update(instance, validated_data)

        
# Image Serializer
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['idimage', 'image']     



# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'last_name', 'email','first_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            password=validated_data['password']
        )

        return user
# User Serializer
class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('id', 'username','last_name', 'email','first_name')

# Change Password
from rest_framework import serializers
from django.contrib.auth.models import User

class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)