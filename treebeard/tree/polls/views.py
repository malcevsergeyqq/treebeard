from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Category
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .serializers import UserSerializer, CategorySerializer
from rest_framework import viewsets, status


get = lambda node_id: Category.objects.get(pk=node_id)


def make_tree():
    root = Category.add_root(name='Computer Hardware')
    node = get(root.pk).add_child(name='Memory')
    get(node.pk).add_sibling(name='Hard Drives')
    get(node.pk).add_sibling(name='SSD')
    get(node.pk).add_child(name='Desktop Memory')
    get(node.pk).add_child(name='Laptop Memory')
    get(node.pk).add_child(name='Server Memory')
    Desktop_Memory = Category.objects.get(id=5)
    get(Desktop_Memory.id).add_child(name='RGB DDR4 SD RAM DDR4 3200')
    get(Desktop_Memory.id).add_child(name='RGBA DDR3 SD RAM DDR4 2400')
    get(Desktop_Memory.id).add_child(name='8GB Single DDR3/DDR3L 1600')


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TreeDataViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def list(self, request):
        if not Category.get_tree().filter(depth=1):
            make_tree()
            return Response(Category.dump_bulk(), status=status.HTTP_201_CREATED)

        return Response(Category.dump_bulk(), status=status.HTTP_200_OK)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def list(self, request):
        return Response(Category.dump_bulk(), status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        queryset = Category.get_tree().filter(depth=1, depth__isnull=True)
        operation = get_object_or_404(queryset, pk=pk)
        serializer = Category(operation, context={'request': request})

        return Response(serializer.data)

    def update(self, request, pk=None):
        serializer = CategorySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data)

    def destroy(self, request, pk=None):
        get(pk).delete()

        return Response(Category.dump_bulk())