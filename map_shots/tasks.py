from celery.task import task
from django.core.files.base import ContentFile

from map_shots.api import YandexStaticMap
from map_shots.models import Shot, ShotPart


@task()
def make_shot():
    lng_offset = 0.002403
    lat, lng = [20.512733, 54.710454]

    shot = Shot(latlng=[lat, lng])
    shot.save()

    idx = 0

    # for i in range(10):
    for j in range(10):
        new_lng = lng + (j * lng_offset)
        result_bytes = YandexStaticMap.get_image([
            lat,
            new_lng
        ])
        shotpart = ShotPart(
            number=idx,
            shot=shot,
            latlng=[lat, new_lng]
        )
        shotpart.image.save(
            f'{j}-{"-".join(map(str, (lat, new_lng)))}.png',
            ContentFile(result_bytes),
            save=True
        )
        idx += 1
