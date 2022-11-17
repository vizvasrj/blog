from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("login/", views.user_login, name="login"),
    path("register/", views.register, name="register"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("edit/", views.profile_edit, name="profile_edit"),
    path('logout/', auth_views.LogoutView.as_view( template_name='registration/logout.html' ), name='logout'),
    path("<slug:slug>/", views.user_detail, name="user_detail"),

    # 

]