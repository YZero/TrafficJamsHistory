from celery.task import task
from django.core.files.base import ContentFile

from map_shots.api import YandexStaticMap
from map_shots.models import Shot, ShotPart


@task()
def make_shot():
    lng_offset = 0.022403
    lat, lng = [20.512733, 54.710454]

    shot = Shot(latlng=[lat, lng])
    shot.save()

    # for i in range(10):
    for j in range(10):
        new_lng = lng + (j * lng_offset)
        result_bytes = YandexStaticMap.get_image([
            lat,
            new_lng
        ])
        shotpart = ShotPart(
            shot=shot,
            latlng=[lat, new_lng]
        )
        shotpart.image.save(
            ContentFile(result_bytes),
            f'{map(str, (lat, new_lng))}.png',
            save=True
        )
