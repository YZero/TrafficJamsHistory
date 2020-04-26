import os
from datetime import (
    datetime,
)

import cv2
from django.conf import (
    settings,
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
)
from django.http import (
    HttpResponseRedirect,
)
from django.views import (
    View,
)

from map_shots.mixins import (
    JSONResponseMixin,
)
from map_shots.models import (
    Shot,
)


def compile_video(images, fps=5):
    filename = f'{datetime.now()}.mp4'
    path_out = os.path.join(settings.MEDIA_ROOT, filename)

    img = cv2.imread(os.path.join(settings.MEDIA_ROOT, images[0].image))
    height, width, _ = img.shape

    out = cv2.VideoWriter(
        path_out,
        cv2.VideoWriter_fourcc(*'MP4V'),
        fps,
        (width, height),
    )

    for idx, image_object in enumerate(images):
        file_path = os.path.join(settings.MEDIA_ROOT, image_object.image)

        if os.path.isfile(file_path):
            img = cv2.imread(file_path)
            img = cv2.putText(
                img,
                f'{image_object.created}',
                org=(250, 350),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=3,
                color=(0, 0, 0),
                thickness=4,
                lineType=cv2.LINE_AA,
            )

            out.write(img)

    out.release()
    return filename


class ShotListView(JSONResponseMixin, View):
    """
    список снимков карт
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
    """
    список комбинаций снимков
    """

    def get_shots(self, filter_kwargs=None):
        return super().get_shots({
            'is_combination': True
        })


class CompileVideoView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        try:
            limit = int(request.GET.get('limit'))
        except TypeError:
            limit = None

        shots = Shot.objects.filter(
            is_combination=False,
        ).values_list(
            'image',
            'created',
            named=True,
        ).order_by(
            'created',
        )

        if limit:
            shots = shots[:limit]

        filename = compile_video(
            shots,
            request.GET.get('fps', 3)
        )
        return HttpResponseRedirect(f'{settings.MEDIA_URL}{filename}')
