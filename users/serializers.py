# users/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    role = serializers.CharField(required=False)
    is_seller = serializers.BooleanField(required=False)
    is_authenticated = serializers.BooleanField(read_only=True)
   
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'role', 'is_seller', 'is_authenticated')

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with that email already exists.")
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with that username already exists.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data.get('role', ''),  # Add role if available
            is_seller=validated_data.get('is_seller', False)  # Add is_seller if available
        )
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role', 'is_seller', 'is_authenticated')
        read_only_fields = ('id', 'is_authenticated')

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'role', 'is_seller')
        extra_kwargs = {
            'email': {'required': True}
        }
