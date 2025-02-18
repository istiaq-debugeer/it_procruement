# user/views.py
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser
from .serializers import CustomUserSerializer


class UserCreateView(generics.CreateAPIView):

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class UserListView(generics.ListAPIView):

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    # permission_classes = [IsAuthenticated]  # Only authenticated users can view the list


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [
        IsAuthenticated
    ]  # Only authenticated users can perform these actions
    lookup_field = "uuid"  # Use UUID as the lookup field
