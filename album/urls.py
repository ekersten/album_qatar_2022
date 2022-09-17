from django.urls import path, include

from .views import GroupsView

urlpatterns = [
    path('api/', include('album.api.urls')),
    path('', GroupsView.as_view(), name='groups'),
]
