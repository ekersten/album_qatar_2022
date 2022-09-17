from django.urls import path

from .views import CreateStickerAPIView, DeleteStickerAPIView

urlpatterns = [
    path('add_sticker/', CreateStickerAPIView.as_view()),
    path('delete_sticker/', DeleteStickerAPIView.as_view()),
]
