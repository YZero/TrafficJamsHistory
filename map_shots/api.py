import math
from collections import namedtuple
from decimal import Decimal
from io import BytesIO
from itertools import product

import requests
from PIL import Image
from django.conf import settings
from django.core.files.base import ContentFile
from more_itertools import grouper


class YandexStaticMap:
    url = settings.YANDEX_STATIC_MAP_API_URL
    layers = (
        'map',
        'trf',
    )
    zoom = 14
    lat_offset = Decimal(0.05574)
    lng_offset = Decimal(0.02234)
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

    @classmethod
    def make_complex_image(cls, file_objects_list, latitude_width):
        """
        Формирует большой снимок из частей

        снизу ^ вверх, слева -> направо
        """
        # расчёт количества изображений по широте
        blocks_count = math.ceil(
            (latitude_width + cls.lat_offset) / cls.lat_offset
        )

        chunks = grouper(
            iterable=file_objects_list,
            n=blocks_count,
        )
        chunks = list(chunks)

        total_width = YandexStaticMap.size[0] * blocks_count
        total_height = YandexStaticMap.size[1] * len(chunks)

        image = Image.new('RGB', (total_width, total_height))

        y_offset = YandexStaticMap.size[1]
        for idx, chunk in enumerate(chunks):
            images = list(map(Image.open, filter(lambda x: x, chunk)))

            x_offset = 0
            for im in images:
                image.paste(im, (x_offset, total_height - y_offset))
                x_offset += im.size[0]

            y_offset += YandexStaticMap.size[1]

        buffer = BytesIO()
        image.save(fp=buffer, format='JPEG')
        return ContentFile(buffer.getvalue())
