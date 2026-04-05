from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.views import APIView

from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import Account
from api.serializers.auth_serializer import RegisterSerializer


# 🔥 1. REGISTER API
class RegisterView(generics.CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            "success": True,
            "message": "User registered successfully"
        }, status=status.HTTP_201_CREATED)


# 🔥 2. LOGIN API
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(request, email=email, password=password)

        if user is None:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        })


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        response = Response(
            {"message": "Logged out successfully"},
            status=status.HTTP_200_OK
        )

        # 🔥 get refresh token from cookie
        refresh_token = request.COOKIES.get("refresh_token")

        # 🔐 optional: blacklist token
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception:
                pass  # token invalid ho to ignore

        # 🍪 delete cookie
        response.delete_cookie(
            key="refresh_token",
            path="/",
            samesite="None",
        )

        return response

# 🔥 4. PROFILE API
class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user

        return Response({
            "email": user.email,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
        })