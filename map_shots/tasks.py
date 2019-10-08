from celery.task import task
from django.core.files.base import ContentFile

from map_shots.api import YandexStaticMap
from map_shots.models import Shot, ShotPart


@task()
def make_shot():
    start_point = [20.440116, 54.768185]
    end_point = [20.604260, 54.649918]

    point_list = YandexStaticMap.create_point_list(
        start_point,
        end_point,
    )

    shot = Shot(
        start_latlng=start_point,
        end_latlng=end_point,
    )
    shot.save()

    for idx, point in enumerate(point_list):
        result_bytes = YandexStaticMap.get_image(lanlng=point)
        shotpart = ShotPart(
            number=idx,
            shot=shot,
            latlng=point,
        )
        shotpart.image.save(
            f'{idx}-{"-".join(map(str, point))}.png',
            ContentFile(result_bytes),
            save=True
        )

    shot.join_shotparts()
