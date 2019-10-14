from celery.task import task
from django.core.files.base import ContentFile

from map_shots.api import YandexStaticMap
from map_shots.models import Shot, ShotPart, GeoSquare


@task()
def make_shots():
    """
    Сделать снимки квадратов
    """
    for square in GeoSquare.enabled_squares.all():
        print(f'square {square}')

        point_list = YandexStaticMap.create_point_list(
            square.start_point,
            square.end_point,
        )

        shot = Shot(
            square=square,
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
