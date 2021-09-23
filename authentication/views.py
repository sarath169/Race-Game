import json
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status

from .serializers import RegisterSerializer, PasswordChangeSerializer

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
        def post(self, request):
                print(request.data)
                username = request.data['username']
                password = request.data['password']
                print(username, password)
                try:
                        user = authenticate(username = username, password = password)
                        print(user)
                        token = Token.objects.get_or_create(user = user)
                        print(token[0])
                        return Response({'token' : str(token[0]), 'id': user.id}, status=status.HTTP_200_OK)
                except Exception as e:
                        print(e)
                        return Response({'error': str(e)}, status = status.HTTP_404_NOT_FOUND)
                
                

class LogoutView(APIView):
        # This view is to logout uers
        def post(self, request, format=None):
                print(request.data['user'])
                try:
                        # simply delete the token to force a login
                        username = request.data['user']
                        print(username)
                        user = User.objects.get(username = username)
                        user.auth_token.delete()
                        data = {"message":"logout success"}
                        return Response(data, status=status.HTTP_200_OK)
                except:
                        message = {"message" : "Token not found" }
                        return Response(message, status=status.HTTP_404_NOT_FOUND)

class PasswordChangeView(APIView):
        
        def post(self, request):
                print(request.data['username'], request.data['newpassword'], request.data['newpassword2'])
                try:
                        # simply delete the token to force a login
                        username = request.data['username']
                        newpassword = request.data['newpassword']
                        newpassword2 = request.data['newpassword2']
                        user = User.objects.get(username = username)
                        
                        if newpassword == newpassword2:
                                user.set_password(newpassword)
                                user.save()
                                return Response({"response" : "Password change Success"}, status = status.HTTP_200_OK)
                        else:
                                return Response({"response" : "Passwords do not match"}, status = status.HTTP_200_OK)
                except Exception as e:
                        print(e)
                        message = {"message" : "user not found" }
                        return Response(message, status=status.HTTP_404_NOT_FOUND)

