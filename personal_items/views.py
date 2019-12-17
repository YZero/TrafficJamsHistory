import os

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from django.views.generic import ListView, CreateView
from xhtml2pdf import pisa

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


class PdfPrintView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    @staticmethod
    def link_callback(uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those
        resources
        """
        sUrl = settings.STATIC_URL
        sRoot = settings.STATIC_ROOT
        mUrl = settings.MEDIA_URL
        mRoot = settings.MEDIA_ROOT

        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri

        if not os.path.isfile(path):
            raise Exception(f'media URI must start with {sUrl} or {mUrl}')
        return path

    def get(self, request, *args, **kwargs):
        template_path = 'pdf_template.html'
        context = {
            'personal_things': PersonalThing.objects.all(),
        }

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="report.pdf"'

        template = get_template(template_path)
        html = template.render(context)

        # create a pdf
        pisa_status = pisa.CreatePDF(
            html,
            dest=response,
            link_callback=self.link_callback,
        )
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response
