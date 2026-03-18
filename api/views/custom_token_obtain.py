from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status
class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response=super().post(request, *args, **kwargs)
        if response.status_code==200:
            refresh=response.data.get("refresh")
            access=response.data.get("access")
            res = Response(
                {"access": access},  # 👈 sirf access return karna
                status=status.HTTP_200_OK,
            )
            print("Refresh token",refresh)
            res.set_cookie(
                key="refresh_token",
                value=refresh,
                httponly=True,
                secure=False,  # 🔥 production me True karna
                samesite="Lax",
                max_age=7 * 24 * 60 * 60,  # 7 days
            )
            return res
        return response