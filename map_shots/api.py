from collections import namedtuple
from itertools import product

import requests

from django.conf import settings


class YandexStaticMap:
    url = settings.YANDEX_STATIC_MAP_API_URL
    layers = (
        'map',
        'trf',
    )
    zoom = 14
    lat_offset = 0.055
    lng_offset = 0.0225
    size = (650, 450)

    Point = namedtuple('Point', 'latitude longitude')

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

    @classmethod
    def create_point_list(
            cls,
            start_point_ll,
            end_point_ll,
    ):
        """
        Создаст набор точек между от старта до финиша
        :param list start_point_ll: [latitude, longitude]
        :param list end_point_ll: [latitude, longitude]
        :return:
        """
        start_point = cls.Point(*start_point_ll)
        end_point = cls.Point(*end_point_ll)

        latitudes = list(sorted([start_point.latitude, end_point.latitude]))
        longitudes = list(sorted([start_point.longitude, end_point.longitude]))

        while latitudes[-2] < latitudes[-1]:
            latitudes.insert(-1, latitudes[-2] + cls.lat_offset)

        while longitudes[-2] < longitudes[-1]:
            longitudes.insert(-1, longitudes[-2] + cls.lng_offset)

        # уберём последнюю точку т.к. не нужна
        latitudes.pop()
        longitudes.pop()

        return list(sorted(
            product(latitudes, longitudes),
            key=lambda x: x[1]
        ))


def make_complex_image(images_paths_list):
    print(images_paths_list)
