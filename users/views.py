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
    template_name = 'users/signup.html'

    def get(self, request):
        return render(request, template_name=self.template_name)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return render(request, self.template_name, {'error_message': serializer.errors, 'data': request.data})


class LoginView(CreateAPIView):
    serializer_class = LoginUserSerializer
    permission_classes = (permissions.AllowAny,)
    template_name = 'users/login.html'

    def get(self, request):
        return render(request, template_name=self.template_name)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            login(request=self.request, user=serializer.save())
            return Response({"message": "Авторизация прошла успешно."})
        return render(request, self.template_name, {"error_message": serializer.errors})


class ProfileView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)
    template_name = 'users/profile.html'

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        user = request.user
        return render(request, self.template_name, {'user': user})

    def perform_destroy(self, instance):
        logout(self.request)


class UpdatePasswordView(UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = UpdatePasswordSerializer
    template_name = 'users/update_password.html'

    def get(self, request):
        return render(request, self.template_name)
