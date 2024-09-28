from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from django.contrib.auth.hashers import make_password

User = get_user_model()

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'role', 'status', 'mobile_number', 'profile_photo']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            name=validated_data['name'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data['role'],
            mobile_number=validated_data['mobile_number'],
        )
        return user

# Login Serializer
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        user = authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        return user

# Change Password Serializer
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect")
        return value

    def validate_new_password(self, value):
        # Add your custom password validation here
        return value

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
