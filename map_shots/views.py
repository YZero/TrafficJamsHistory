from django.views import View

from map_shots.mixins import JSONResponseMixin
from map_shots.models import Shot


class ShotListView(JSONResponseMixin, View):
    """
    список карт
    """

    def get_offset_limit_parameters(self, request):
        try:
            offset = int(request.GET.get('offset'))
        except (ValueError, TypeError):
            offset = 0

        try:
            limit = int(request.GET.get('limit'))
        except (ValueError, TypeError):
            limit = 200
        return offset, limit

    def get_shots(self, filter_kwargs=None):
        if not filter_kwargs:
            filter_kwargs = {}
        shots = Shot.objects.filter(**filter_kwargs)
        return shots

    def get(self, request, *args, **kwargs):
        offset, limit = self.get_offset_limit_parameters(request)

        shots = self.get_shots({
            'is_combination': False
        })[offset:offset + limit]

        shots_result = [
            {
                'id': shot.id,
                'created': shot.created,
                'image': (
                    request.build_absolute_uri(shot.image.url)
                    if shot.image else None
                ),
            } for shot in shots
        ]
        return self.render_to_json_response(context={
            'shots': shots_result,
        })


class ShotCombinationListView(ShotListView):

    def get_shots(self, filter_kwargs=None):
        return super().get_shots({
            'is_combination': True
        })
