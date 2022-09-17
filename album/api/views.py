from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from ..models import Sticker
from .serializers import GenericStickerSerializer, StickerSerializer


class CreateStickerAPIView(APIView):
    def post(self, request):
        serializer = StickerSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            sticker = Sticker.objects.create(
                team=serializer.validated_data.get('team'),
                number=serializer.validated_data.get('number')
            )

            return Response(data=StickerSerializer(instance=sticker).data, status=status.HTTP_201_CREATED)


class DeleteStickerAPIView(APIView):
    def post(self, request):
        serializer = GenericStickerSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            sticker = Sticker.objects.filter(
                team=serializer.validated_data.get('team'),
                number=serializer.validated_data.get('number')
            ).first()

            if sticker:
                sticker.delete();
                return Response(data={}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(data={}, status=status.HTTP_404_NOT_FOUND)
