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

    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(self.object, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.object.set_password(serializer.validated_data['new_password'])
        self.object.save()
        return Response({"detail": "Password changed successfully."}, status=status.HTTP_200_OK)    

