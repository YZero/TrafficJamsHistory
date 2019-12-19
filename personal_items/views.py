import locale
from itertools import zip_longest

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.views import View
from django.views.generic import ListView, CreateView, TemplateView

from map_shots.mixins import JSONResponseMixin
from personal_items.forms import PersonalThingForm
from personal_items.models import Nomenclature, Unit, PersonalThing


def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


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


class PdfPrintView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'pdf_template.html'

    def get(self, request, *args, **kwargs):
        first_page_count = 12
        next_page_count = int(request.GET.get('next_page_count', 23))

        if not self.extra_context:
            self.extra_context = {}

        locale.setlocale( locale.LC_ALL, '' )
            
        grouped_things = [
            dict(
                item, 
                counter=idx, 
                cost=locale.currency(
                    item['cost'],
                    symbol=False, 
                    grouping=True,
                )
            )
            for idx, item in enumerate(
                PersonalThing.objects.order_by(
                    'nomenclature__name',
                    'unit__name',
                ).values(
                    'nomenclature__name',
                    'unit__name',
                ).annotate(
                    quantity=Sum('quantity'),
                    cost=Sum('cost'),
                ),
                start=1,
            )
        ]

        pages = grouper(grouped_things[first_page_count:], next_page_count)

        self.extra_context.update({
            'first_things': grouped_things[:first_page_count],
            'next_things_pages': pages,
        })
        return super().get(request, *args, **kwargs)
