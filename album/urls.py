from django.urls import path, include

from .views import MarkView, MissingStickersView, StatsView

urlpatterns = [
    path('api/', include('album.api.urls')),
    path('', MissingStickersView.as_view()),
    path('mark/', MarkView.as_view()),
    path('stats/', StatsView.as_view()),
]
