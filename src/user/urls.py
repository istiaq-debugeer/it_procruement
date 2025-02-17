# user/urls.py
from django.urls import path
from .views import UserCreateView, UserListView, UserDetailView

urlpatterns = [
    path("create/", UserCreateView.as_view(), name="user-create"),
    path("list/", UserListView.as_view(), name="user-list"),
    path("<uuid:uuid>/", UserDetailView.as_view(), name="user-detail"),
]
