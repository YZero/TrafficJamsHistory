from django.db.models import Manager


class GeoSquareManager(Manager):

    def get_queryset(self):
        return super().get_queryset().filter(
            enabled=True,
        )
