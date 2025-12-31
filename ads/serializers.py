from rest_framework import serializers
from .models import Ad


class AdSerializers(serializers.ModelSerializer):
    publisher = serializers.ReadOnlyField(source='publisher.username')

    class Meta:
        model = Ad
        fields = '__all__'
        read_only_fields = ('date_added', 'is_public', 'id')
        extra_kwargs = {
            'image': {'required': False}
        }
    