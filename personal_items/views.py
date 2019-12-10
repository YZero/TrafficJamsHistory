from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import ListView, CreateView

from map_shots.mixins import JSONResponseMixin
from personal_items.forms import PersonalThingForm
from personal_items.models import Nomenclature, Unit, PersonalThing


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


class PersonalThingsFormView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'personal_things_form.html'
    form_class = PersonalThingForm
    success_url = '/add/'

    def get_form_kwargs(self):
        f_kwargs = super().get_form_kwargs()

        if 'data' in f_kwargs:
            data = f_kwargs['data'].copy()

            if not data['nomenclature'] and data['nomenclature_name']:
                new_nomenclature = Nomenclature.objects.create(
                    name=data['nomenclature_name']
                )
                data['nomenclature'] = new_nomenclature.id
                f_kwargs['data'] = data

            if not data['unit'] and data['unit_name']:
                new_unit = Unit.objects.create(
                    name=data['unit_name']
                )
                data['unit'] = new_unit.id
                f_kwargs['data'] = data

        return f_kwargs


class PersonalThingsListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = PersonalThing
    template_name = 'personal_things_list.html'
