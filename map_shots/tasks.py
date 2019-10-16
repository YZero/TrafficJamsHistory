from celery.task import task

from map_shots.models import GeoSquare


@task()
def make_shots():
    """
    Сделать снимки квадратов
    """
    for square in GeoSquare.enabled_squares.all():
        square.make_shot()
