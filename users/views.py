from django.contrib.auth import login, logout
from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.response import Response

from users.models import User
from users.serializers import CreateUserSerializer, LoginUserSerializer, ProfileSerializer, UpdatePasswordSerializer


class SignupView(CreateAPIView):
    serializer_class = CreateUserSerializer
    permission_classes = (permissions.AllowAny,)

    def get(self, request, *args, **kwargs):
        return render(request, 'users/signup.html')

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return render(request, 'users/signup.html', {'form': serializer.errors, 'data': request.data})


class LoginView(CreateAPIView):
    serializer_class = LoginUserSerializer
    permission_classes = (permissions.AllowAny,)

    def get(self, request, *args, **kwargs):
        return render(request, 'users/login.html')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        login(request=self.request, user=serializer.save())


class ProfileView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        user = request.user
        return render(request, 'users/profile.html', {'user': user})

    def perform_destroy(self, instance):
        logout(self.request)


class UpdatePasswordView(UpdateAPIView):
    # permission_classes = (permissions.IsAuthenticated, )
    serializer_class = UpdatePasswordSerializer

    def get(self, request, *args, **kwargs):
        return render(request, 'update_password.html')
