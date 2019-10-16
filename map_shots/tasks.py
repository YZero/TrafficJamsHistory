from celery.task import task

from map_shots.models import GeoSquare


@task()
def make_shots(square_id=None):
    """
    Сделать снимки квадратов
    """
    squares = GeoSquare.enabled_squares.all()

    if square_id:
        squares = squares.filter(id=square_id)

    for square in squares:
        square.make_shot()
