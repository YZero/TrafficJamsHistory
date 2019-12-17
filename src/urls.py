from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

from map_shots.views import ShotListView, ShotCombinationListView
from personal_items.views import (
    NomenclatureListView, UnitListView,  PersonalThingsFormView,
    PersonalThingsListView, PdfPrintView,
)

urlpatterns = [
    path('', ShotListView.as_view(), name='shot_list'),
    path('combinations/',
         ShotCombinationListView.as_view(),
         name='combinations_list'),
    # ----------- Личные вещи --------------
    path('nomenclature/',
         NomenclatureListView.as_view(),
         name='nomenclature_list'),
    path('units/',
         UnitListView.as_view(),
         name='unit_list'),
    path('list/',
         PersonalThingsListView.as_view(),
         name='personal_things'),
    path('add/',
         PersonalThingsFormView.as_view(),
         name='add_personal_thing'),
    path('pdf/',
         PdfPrintView.as_view(),
         name='print_pdf'),
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(), name='login_url'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
