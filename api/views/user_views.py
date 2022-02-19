from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import status

from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from api.models import *
from api.serializers import UserSerializer,UserSerializerWithToken
from ..prevent import UserLoginRateThrottle

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
       
        serializer = UserSerializerWithToken(self.user).data

        for k,v in serializer.items():
            data[k] =v

        return data
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['message'] = "Hello"

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    throttle_classes = (UserLoginRateThrottle,)
    serializer_class = MyTokenObtainPairSerializer


@api_view(['GET'])
def getRoutes(request):
    routes =[
        '/api/products/',
        '/api/products/<id>',
        '/api/users',
        '/api/users/register',
        '/api/users/login',
        '/api/users/profile',
    ]
    return Response(routes)


@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        'name': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        'password': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        'email': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
    }
))
@api_view(['POST'])
def registerUser(request):
    data = request.data
    try:
        user = User.objects.create(
            first_name = data['name'],
            username = data['email'],
            password = make_password(data['password']),
            email = data['email'],
        )

        serializer = UserSerializerWithToken(user,many=False)
        return Response(serializer.data)
    
    except:
        message = {"detail":"User with this email is already registered"}
        return Response(message,status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user =request.user 
    serializer = UserSerializer(user,many = False)
    return Response(serializer.data)


@swagger_auto_schema(method='put', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        'name': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        'password': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        'email': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
    }
))
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserProfile(request):
    user =request.user 
    serializer = UserSerializerWithToken(user,many = False)
    data = request.data
    user.first_name = data['name']
    user.username = data['email']
    user.email = data['email']
    if data['password'] !="":
        user.password= make_password(data['password'])
    user.save()
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users,many = True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUserById(request,pk):
    users = User.objects.get(id=pk)
    serializer = UserSerializer(users,many = False)
    return Response(serializer.data)


@swagger_auto_schema(method='put', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        'name': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        'email': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        'isAdmin': openapi.Schema(type=openapi.TYPE_STRING, description='0/1'),
    }
))
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUser(request,pk):
    user =User.objects.get(id=pk)
   
    data = request.data
    user.first_name = data['name']
    user.username = data['email']
    user.email = data['email']
    user.is_staff = data['isAdmin']
    
    user.save()
    serializer = UserSerializer(user,many = False)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteUser(request,pk):
    userForDeletion = User.objects.get(id=pk)
    userForDeletion.delete()
    return Response("User was deleted")