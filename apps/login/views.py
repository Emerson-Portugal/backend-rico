from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.shortcuts import get_object_or_404

from apps.produccion.pagination import CustomPagination
from .models import CustomUser
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny



@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response(
            {"error": "Username and password are required."},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        user = CustomUser.objects.get(username=username)
    except CustomUser.DoesNotExist:
        return Response(
            {"error": "User does not exist."},
            status=status.HTTP_404_NOT_FOUND
        )

    if not user.check_password(password):
        return Response(
            {"error": "Invalid password."},
            status=status.HTTP_401_UNAUTHORIZED
        )

    token, _ = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(user)

    return Response({
        "data": {
            "token": token.key,
            "user": serializer.data
        }
    }, status=status.HTTP_200_OK)


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


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def profile(request):
    return Response({
        "data": {
            "username": request.user.username,
            "full_name": request.user.full_name,
            "role": request.user.role
        },
        "httpStatusCode": 200,
        "isSuccess": True,
        "messages": []
    }, status=200)




@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_all_users(request):
    users = CustomUser.objects.all()
    paginator = CustomPagination()
    result_page = paginator.paginate_queryset(users, request)
    serializer = UserSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_user_by_id(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    serializer = UserSerializer(user)
    return Response({"data": serializer.data}, status=200)



@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    # Solo ADMIN puede modificar a otros usuarios
    #if request.user.role != 'ADMIN':
    #   return Response({"error": "Unauthorized"}, status=403)

    data = request.data
    if 'username' in data:
        user.username = data['username']
    if 'role' in data:
        user.role = data['role']
    if 'password' in data:
        user.set_password(data['password'])

    user.save()
    serializer = UserSerializer(user)
    return Response({"data": serializer.data}, status=200)


@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    # Solo ADMIN puede eliminar
    #if request.user.role != 'ADMIN':
    #   return Response({"error": "Unauthorized"}, status=403)

    user.delete()
    return Response({"message": f"User {user_id} deleted successfully."}, status=200)
