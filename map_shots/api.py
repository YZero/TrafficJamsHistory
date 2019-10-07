import requests

from django.conf import settings


class YandexStaticMap:
    url = settings.YANDEX_STATIC_MAP_API_URL
    layers = (
        'map',
        'trf',
    )
    zoom = 14
    size = (650, 450)

    @classmethod
    def get_image(
            cls,
            lanlng,
            zoom=None,
            layers=None,
            size=None,
    ):
        """
        :param tuple|list lanlng:
        :param int zoom:
        :param list[str] layers:
        :param list[int] size:
        :return:
        """
        request = requests.get(
            cls.url,
            params={
                'll': ','.join(map(str, lanlng)),
                'z': f'{zoom or cls.zoom}',
                'l': ','.join(layers or cls.layers),
                'size': ','.join(map(str, size or cls.size)),
            }
        )
        return request.content
