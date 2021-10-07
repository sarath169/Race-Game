import random
import threading

from django.shortcuts import render
from django.contrib.auth import authenticate
from django.core.mail import EmailMessage, message
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status

from .models import UserOtp
from .serializers import RegisterSerializer, PasswordChangeSerializer
from django.conf import settings

class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email=email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()

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
                        return Response({'error': "password does not match"}, status = status.HTTP_400_BAD_REQUEST)
                
                

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

class SendMailView(APIView):
        def post(self, request):
                otp = random.randrange(99999, 999999)
                username = request.data['username']
                user = User.objects.get(username = username)
                if user:
                        subject = 'Teletyping App  : OTP to change password'
                        # message = render_to_string('OTP to verify ', otp)
                        email_from = settings.EMAIL_HOST_USER
                        print(email_from)
                        to=user.email
                        print(to)
                        try:
                                userotp_obj = UserOtp.objects.get(user = user.id)
                        except:
                                userotp_obj = None
                        if userotp_obj:
                                email= EmailMessage(
                                        subject,        
                                        userotp_obj.otp,
                                        email_from,
                                        [to],
                                )
                        else:
                                email= EmailMessage(
                                                subject,        
                                                str(otp),
                                                email_from,
                                                [to],
                                        )
                                userotp_obj = UserOtp(user_id = user.id, otp = otp)
                                userotp_obj.save()
                else:
                        response = {"message" : "user with email not found" }
                        return Response(response, status=status.HTTP_404_NOT_FOUND)
                EmailThread(email).run()
                message = {"message" : "success" }
                return Response(message, status=status.HTTP_200_OK)

class VerifyOtpView(APIView):
        def post(self, request):
                try:
                        email = request.data['email']
                        otp = request.data['otp']
                        user = User.objects.get(email = email)
                        userotp_obj = UserOtp.objects.get(user = user.id)
                        print(userotp_obj.otp)
                        print(otp)
                        if userotp_obj.otp == otp:
                                k =UserOtp.objects.filter(user = user.id).delete()
                                print(k)
                                return Response({"response" : "Validation success"}, status=status.HTTP_200_OK)
                        else:
                                return Response({"error" : "otp did not match"}, status=status.HTTP_401_UNAUTHORIZED)

                except Exception as e:
                        print(e)
                        message = {"message": "check formdata"}
                        return Response({"response" : "Password change Success"}, status = status.HTTP_400_BAD_REQUEST)


class ForgotPasswordView(APIView):
        def post(self, request):
                print(request.data['username'], request.data['newpassword'], request.data['repeatpassword'])
                try:
                        # simply delete the token to force a login
                        username= request.data['username']
                        newpassword = request.data['newpassword']
                        repeat_password = request.data['repeatpassword']
                        user = User.objects.get(username = username)
                        
                        if newpassword == repeat_password:
                                user.set_password(newpassword)
                                user.save()
                                return Response({"response" : "Password change Success"}, status = status.HTTP_200_OK)
                        else:
                                return Response({"response" : "Passwords do not match"}, status = status.HTTP_200_OK)
                except Exception as e:
                        print(e)
                        message = {"message" : "user not found" }
                        return Response(message, status=status.HTTP_404_NOT_FOUND)
