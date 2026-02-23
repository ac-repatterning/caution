"""Module backgrounds.py"""

import logging

import boto3

import config
import src.elements.background as bck
import src.functions.secret


class Backgrounds:
    """
    The base-layer-maps list.
    """

    def __init__(self, connector: boto3.session.Session):
        """

        :param connector: An instance of boto3.session.Session
        """

        # Secrets
        self.__secret = src.functions.secret.Secret(connector=connector)

    def __get_dictionary(self):
        """
        Note, the option with filename = `assets` is temporary; it will be removed after the new set-up is
        in place.

        :return:
        """

        e_technologies = self.__secret.exc(secret_id=config.Config().project_key_name, node='europa-technologies')

        dictionary = [
            {'tiles': 'https://tile.viaeuropa.uk.com/' +  e_technologies + '/m0306/{z}/{x}/{y}.png',
             'attr': '© Europa Technologies Ltd. Contains Ordnance Survey data © Crown copyright and database',
             'filename': 'vml-spm-f-raster-ordnance-survey',
             'zoom_start': 8, 'min_zoom': 8, 'max_zoom': 17, 'crs': 'EPSG3857'},
            {'tiles': 'https://tile.viaeuropa.uk.com/' +  e_technologies + '/m0310/{z}/{x}/{y}.png',
             'attr': '© Europa Technologies Ltd. Contains Ordnance Survey data © Crown copyright and database',
             'filename': 'mm-spm-ordnance-survey',
             'zoom_start': 7, 'min_zoom': 7, 'max_zoom': 17, 'crs': 'EPSG3857'},
            {'tiles': 'https://tile.viaeuropa.uk.com/' +  e_technologies + '/m0301/{z}/{x}/{y}.png',
             'attr': '© Europa Technologies Ltd. Contains Ordnance Survey data © Crown copyright and database',
             'filename': 'vml-spm-f-vector-ordnance-survey',
             'zoom_start': 7, 'min_zoom': 7, 'max_zoom': 17, 'crs': 'EPSG3857'},
            {'tiles': 'OpenStreetMap',
             'attr': None,
             'filename': 'open-street-map', 'zoom_start': 7,  'min_zoom': 0, 'max_zoom': 19, 'crs': 'EPSG3857'},
            {'tiles': 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}.png',
             'attr': 'Tiles &copy; Esri &mdash; Esri',
             'filename': 'esri', 'zoom_start': 7, 'min_zoom': 7, 'max_zoom': 19, 'crs': 'EPSG3857'}
        ]

        return dictionary

    def __call__(self) -> list[bck.Background]:
        """
        Background = collections.namedtuple(
            typename = 'Background',
            field_names=['tiles', 'attr', 'filename', 'zoom_start', 'min_zoom', 'max_zoom', 'crs'], defaults={'attr': None})

        :return:
        """

        dictionary = self.__get_dictionary()
        __backgrounds = [bck.Background(**elements) for elements in dictionary]

        for background in __backgrounds:
            logging.info(background.filename)

        return __backgrounds
