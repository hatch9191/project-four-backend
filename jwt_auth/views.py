from datetime import datetime, timedelta
from inspect import currentframe
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth import get_user_model
from django.conf import settings
import jwt

from .serializers import (
    UserRegisterSerializer,
    UserProfileSerializer,
    UserUpdateSerializer,
    BasicProfileSerializer
)

User = get_user_model()


class RegisterView(APIView):

    def post(self, request):
        user_to_create = UserRegisterSerializer(data=request.data)
        if user_to_create.is_valid():
            user_to_create.save()
            return Response(
                {'message': 'Registration Successful'},
                status=status.HTTP_201_CREATED
            )
        return Response(user_to_create.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class LoginView(APIView):

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        try:
            user_to_login = User.objects.get(username=username)
        except User.DoesNotExist:
            raise PermissionDenied(detail='Unauthorized')
        if not user_to_login.check_password(password):
            raise PermissionDenied(detail='Unauthorized')
        expiry_time = datetime.now() + timedelta(days=7)
        token = jwt.encode(
            {'sub': user_to_login.id,
             'exp': int(expiry_time.strftime('%s'))
             },
            settings.SECRET_KEY,
            algorithm='HS256'
        )
        return Response({
            'token': token,
            'message': f'Welcome back, {username}!'
        }, status=status.HTTP_200_OK)


class UserListView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, _request):
        users = User.objects.all()
        serialized_user = BasicProfileSerializer(users, many=True)
        return Response(serialized_user.data, status=status.HTTP_200_OK)


class ProfileUpdateView(UpdateAPIView):

    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = (IsAuthenticated, )


class ProfileEditView(APIView):

    permission_classes = (IsAuthenticated, )

    def put(self, request, **kwargs):
        id = kwargs['pk']
        current_user = User.objects.get(id=request.user.id)
        edited_current_user = UserUpdateSerializer(
            current_user, data=request.data)
        if edited_current_user.is_valid():
            edited_current_user.save()
            return Response(edited_current_user.data, status=status.HTTP_202_ACCEPTED)
        return Response(edited_current_user.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class ProfileView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, _request, user_pk):
        try:
            user_to_show = User.objects.get(pk=user_pk)
        except User.DoesNotExist:
            raise NotFound()
        serialized_user = UserProfileSerializer(user_to_show)
        return Response(serialized_user.data, status=status.HTTP_200_OK)


class UserFollowView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request, pk):
        try:
            user_to_follow = User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound()
        if request.user in user_to_follow.followed_by.all():
            user_to_follow.followed_by.remove(request.user.id)
        else:
            user_to_follow.followed_by.add(request.user.id)
        serialized_followed_user = UserProfileSerializer(user_to_follow)
        return Response(serialized_followed_user.data, status=status.HTTP_202_ACCEPTED)
