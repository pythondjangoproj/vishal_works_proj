from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializer import UserSerializer, RegisterSerializer, Igl_Username_Serializer
from .models import User
from django.core.mail import send_mail
from django.conf import settings


# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


from django.contrib.auth import login

from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)


from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from .serializer import ChangePasswordSerializer
from rest_framework.permissions import IsAuthenticated


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsernameAPI(generics.GenericAPIView):
    serializer_class = Igl_Username_Serializer

    def get(self, request, pk=None):
        user_id = pk
        if user_id is not None:
            user = User.objects.get(id=user_id)
            serializer = Igl_Username_Serializer(user)
            return Response({"data": serializer.data})
        user = User.objects.all()
        serializer = Igl_Username_Serializer(user, many=True)
        return Response({"data": serializer.data})

    def patch(self, request, pk=None):
        user_id = pk
        if user_id is not None:
            user = User.objects.get(id=user_id)
            user.IGL_Username = request.data['IGL_Username']
            user.profile_image = request.data['profile_image']
            user.save()
            return Response({"message": "Successfully Update"})
