from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

# Create your views here.


class GetStackViewWords(APIView):
    
# (Receive token by HTTPS POST)
# ...
    def get(self, request):
        words = ['great', 'welocme', 'wonderful', 'college', 'school']

        return Response({'words' : words}, status= status.HTTP_200_OK)