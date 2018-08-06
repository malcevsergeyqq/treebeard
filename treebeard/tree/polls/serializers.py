# Serializers define the API representation.
from rest_framework import serializers, viewsets, status
from django.contrib.auth.models import User
from polls.models import Category


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    are_children_started = serializers.SerializerMethodField()

    def get_are_children_started(self, obj):
        return all(category.started for category in Category.get_tree(obj))

    class Meta:
        model = Category
        fields = '__all__'
