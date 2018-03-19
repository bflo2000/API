from Amazon.models import Amazon_Variation
from rest_framework import serializers

class Amazon_Variation_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Amazon_Variation
        fields = '__all__'


