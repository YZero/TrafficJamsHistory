from django.views import View

from map_shots.mixins import JSONResponseMixin
from map_shots.models import Shot


class ShotListView(JSONResponseMixin, View):
    """
    список карт
    """

    def get(self, request, *args, **kwargs):
        try:
            offset = int(request.GET.get('offset'))
        except (ValueError, TypeError):
            offset = 0

        try:
            limit = int(request.GET.get('limit'))
        except (ValueError, TypeError):
            limit = 200

        shots = Shot.objects.all()[offset:offset + limit]

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
            'shots': list(shots_result),
        })
