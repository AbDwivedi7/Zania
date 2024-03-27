from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

class LoginView(APIView):
    def post(self, request):
        try:
            username = request.data.get("username")
            password = request.data.get("password")
            
            user = authenticate(username=username, password=password)
            refresh = RefreshToken.for_user(user=user)
            return Response({"refresh": str(refresh), "access": str(refresh.access_token)}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"error": "Username or password is wrong"},status=status.HTTP_401_UNAUTHORIZED)
    
    