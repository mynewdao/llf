from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from category.models import Category
from category.serializers import CategorySerializer


class CreateCategoryAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated,]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer