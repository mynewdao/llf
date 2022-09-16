from django.urls import path
from . import views


urlpatterns = [
    path("categories/", views.CreateCategoryAPIView.as_view())
]