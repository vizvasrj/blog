from django.urls import path
from .views import *
from rest_framework_simplejwt import views as jwt_views



urlpatterns = [
    path('users/', UserListView.as_view(), name='users_list'),
    path('login/', AuthUserLoginView.as_view(), name='users_login'),
    path('logout/', LogoutView.as_view(), name='users_logout'),
    path('register/', AuthUserRegistrationView.as_view(), name='users_register'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='users_token_refresh'),
    path('token/', MyTokenObtainPairView.as_view(), name='users_token'),
]

