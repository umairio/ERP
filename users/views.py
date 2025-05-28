from rest_framework import generics
from .serializers import RegisterSerializer
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework import generics
from users.serializers import CreateProfileSerializer, ChangePasswordSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

User = get_user_model()
class RegisterView(generics.CreateAPIView):
   	serializer_class = RegisterSerializer


class CreateProfileView(generics.CreateAPIView):
    serializer_class = CreateProfileSerializer
    permission_classes = (IsAuthenticated,)

class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def update(self, request):
        user = self.request.user
        serializer = self.get_serializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({"detail": "Password changed successfully."}, status=status.HTTP_201_CREATED)    

