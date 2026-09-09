from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = "authentication"
urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", views.UserProfileView.as_view(), name="auth_user"),
    path("users/", views.UserListView.as_view(), name="show_users"),
    path("users/<int:pk>/", views.UserUpdateView.as_view(), name="show_user"),
]
