from rest_framework import serializers
from .models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')
        extra_kwargs = {
            'id': {
                'read_only': True
            }
        }



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'date', 'price',)
        extra_kwargs = {
            'id': {
                'read_only': True
            }
        }