from rest_framework import serializers

from ..models import Sticker


class StickerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sticker
        fields = ['team', 'number']


class GenericStickerSerializer(serializers.Serializer):
    team = serializers.IntegerField()
    number = serializers.IntegerField()