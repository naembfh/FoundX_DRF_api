from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import UserSerializer, LoginSerializer, ChangePasswordSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.authentication import JWTAuthentication

User = get_user_model()

class UserRegisterView(APIView):
    permission_classes = []  # No restrictions for registration

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Generate tokens using the custom get_token method from User model
            tokens = user.get_token()

            # Return success response with user data and tokens
            return Response({
                'success': True,
                'message': 'User registered successfully',
                'data': tokens  # Contains both access and refresh tokens with custom claims
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'success': False,
            'message': 'Registration failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


# Get All Users (Admin only)
class GetAllUsersView(APIView):
    permission_classes = [IsAdminUser] 

    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Get Single User (Admin or User who owns the account)
class GetSingleUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id, *args, **kwargs):
        try:
            user = User.objects.get(id=id)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)


# Login (Public)
class UserLoginView(APIView):
    permission_classes = []  # Public access to login

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            
            # Generate JWT tokens for the authenticated user
            tokens = user.get_token()

            # Return success response with tokens
            return Response({
                'success': True,
                'message': 'Login successful',
                'data':tokens
            }, status=status.HTTP_200_OK)
        
        return Response({
            'success': False,
            'message': 'Login failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

# Change Password (User or Admin)
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]  # User must be authenticated

    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Password changed successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Refresh Token (Public)
class RefreshTokenView(TokenRefreshView):
    pass
