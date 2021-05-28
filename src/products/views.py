from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import ProductSerializer, CategorySerializer, CategoryCreateSerializer
from .models import Product, Category
from .permissions import IsOwner


class CategoriesListCreateView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryCreateSerializer
    pagination_class = None

    def get_queryset(self):
        return Category.get_ancestors(ascending=False, include_self=False)

    def list(self, request, *args, **kwargs):
        root_nodes = Category.objects.all().get_cached_trees()

        data = []
        for n in root_nodes:
            data.append(self.recursive_node_to_dict(n))

        return Response(data, status=status.HTTP_200_OK)

    def recursive_node_to_dict(self, node):
        result = CategorySerializer(instance=node).data
        children = [self.recursive_node_to_dict(c) for c in node.get_children()]
        if children:
            result["children"] = children
        return result


class ProductListCreateView(ListCreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Product.objects.all()

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class ProductRUDView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner,)
    queryset = Product.objects.all()
    lookup_field = 'id'

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
