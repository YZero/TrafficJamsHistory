from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView

from map_shots.mixins import JSONResponseMixin
from personal_items.models import Nomenclature, Unit


class BaseDictModelListView(JSONResponseMixin, View):
    model = None
    key = ''

    def get(self, request, *args, **kwargs):
        q_filter = {}

        if 'q' in request.GET:
            q_filter = {
                'name__icontains': request.GET['q'],
            }

        nomenclature_qs = self.model.objects.filter(**q_filter)

        nomenclature_result = [
            {
                'id': each.id,
                'name': each.name,
            } for each in nomenclature_qs
        ]
        return self.render_to_json_response(context={
            self.key: nomenclature_result,
        })


class NomenclatureListView(BaseDictModelListView):
    """
    список номенклатуры
    """
    model = Nomenclature
    key = 'nomenclature'


class UnitListView(BaseDictModelListView):
    """
    список единиц измерения
    """
    model = Unit
    key = 'units'


class PersonalThingsFormView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'personal_things_form.html'

    def post(self, request, *args, **kwargs):
        return HttpResponse()
