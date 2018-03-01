from Images.models import Image
from rest_framework import serializers


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'item_sku', 'main_image_url', 'main_image_path', 'category', 'collection', 'sub_collection')


