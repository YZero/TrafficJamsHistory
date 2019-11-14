from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from map_shots.views import ShotListView, ShotCombinationListView

urlpatterns = [
    path('', ShotListView.as_view(), name='shot_list'),
    path('combinations/',
         ShotCombinationListView.as_view(),
         name='combinations_list'),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
