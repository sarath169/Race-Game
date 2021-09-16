import json
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status

from .serializers import RegisterSerializer

# Create your views here.
class RegistrationView(generics.CreateAPIView):
        # This view is to register new users
        serializer_class = RegisterSerializer

        def post(self, request, *args, **kwargs):
                try:
                        serializer = RegisterSerializer(data = request.data)
                        data = {}
                        if serializer.is_valid():
                                serializer.save()
                                data['response'] = "Registration Success"
                        else:
                                data = serializer.errors
                        return Response(data)
                except:
                        message = {"message" : "please provide all necessary values" }
                        return Response(message, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    # permission_classes = [AllowAny]
    def get(self, request):
        username = request.query_params['username']
        password = request.query_params['password']
        print(username, password)
        try:
            user = authenticate(username = username, password = password)
        except Exception as e:
            print(e)
        token = Token.objects.get_or_create(user = user)
        print(token[0])
        return Response({'token' : str(token[0])}, status=status.HTTP_200_OK)

class LogoutView(APIView):
        # This view is to logout uers
        def get(self, request, format=None):
                try:
                        # simply delete the token to force a login
                        request.user.auth_token.delete()
                        data = {"message":"logout success"}
                        return Response(data, status=status.HTTP_200_OK)
                except:
                        message = {"message" : "Token not found" }
                        return Response(message, status=status.HTTP_404_NOT_FOUND)

