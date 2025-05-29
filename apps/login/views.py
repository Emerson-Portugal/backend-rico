from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import CustomUser
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    user = get_object_or_404(CustomUser, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({"error": "Invalid password"}, status=status.HTTP_401_UNAUTHORIZED)

    token, _ = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(user)

    return Response({
        "data": {
            "token": token.key,
            "user": serializer.data
        }
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = CustomUser(
            username=serializer.validated_data['username'],
            role=serializer.validated_data['role']
        )
        user.set_password(serializer.validated_data['password'])
        user.save()

        token = Token.objects.create(user=user)

        return Response({
            "data": {
                "token": token.key,
                "user": UserSerializer(user).data
            }
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def profile(request):
    return Response({
        "data": {
            "username": request.user.username,
            "role": request.user.role
        },
        "httpStatusCode": 200,
        "isSuccess": True,
        "messages": []
    }, status=200)
