from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.contrib.auth import logout
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serilizer import UserSerializer

class RegistrationView(APIView):
    serializer_class = UserSerializer

    def post(self,request):
        serilizer = UserSerializer(data= request.data)
        if serilizer.is_valid():
            account = serilizer.save()
            user_name = serilizer.validated_data['user_name']
            data = { 'response': "user with username " + str(user_name) + ' created'}
            data['key'] = get_object_or_404(Token,user = account).key
            return Response( data ,status = status.HTTP_201_CREATED )
        else :
            return Response(serilizer.errors,status = status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    def get(self,request):
        logout(request)
        return Response({"response" : "logged out"},status=status.HTTP_200_OK)