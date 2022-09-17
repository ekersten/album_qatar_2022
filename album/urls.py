from django.urls import path, include

from .views import MarkView, MissingStickersView

urlpatterns = [
    path('api/', include('album.api.urls')),
    path('', MissingStickersView.as_view()),
    path('mark/', MarkView.as_view()),
]
