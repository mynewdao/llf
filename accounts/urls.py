from django.urls import path
from . import views

urlpatterns = [
    path("registration/", views.UserRegisterAPIView.as_view()),
    path("activation_code/<str:activation_code>/", views.Index.as_view(), name='activate_account'),
    path("login", views.LoginAPIView.as_view(), name='login'),
    path("logout", views.LoginAPIView.as_view(), name='logout'),
]
