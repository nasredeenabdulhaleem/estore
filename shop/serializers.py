#import serializers 
from rest_framework import serializers

from .models import *
# a django serializer for the size model
class size_serializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = "__all__"

# a django serializer for the product variant model
class product_variant_serializer(serializers.ModelSerializer):
    size = size_serializer(many=True)
    class Meta:
        model = ProductVaraiant
        fields = "__all__"
