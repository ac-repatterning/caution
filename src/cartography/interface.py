"""Module interface.py"""

import io

import boto3
import geopandas
import pandas as pd

import src.cartography.illustrate
import src.elements.s3_parameters as s3p
import src.s3.unload


class Interface:
    """
    Interface
    """

    def __init__(self, connector: boto3.session.Session, s3_parameters: s3p.S3Parameters,
                 frame: pd.DataFrame):
        """

        :param connector: A boto3 session instance, it retrieves the developer's <default> Amazon
                          Web Services (AWS) profile details, which allows for programmatic interaction with AWS.
        :param s3_parameters: The overarching S3 parameters settings of this project, e.g., region code
                              name, buckets, etc.
        :param frame: A frame of metrics per gauge instance.
        """

        self.__connector = connector
        self.__s3_parameters = s3_parameters
        self.__frame = frame

    def __get_coarse_boundaries(self) -> geopandas.GeoDataFrame:
        """

        :return:
        """

        __s3_client: boto3.session.Session.client = self.__connector.client(service_name='s3')
        buffer = src.s3.unload.Unload(s3_client=__s3_client).exc(
            bucket_name=self.__s3_parameters.internal, key_name='cartography/coarse.geojson')
        coarse = geopandas.read_file(io.StringIO(buffer))

        return coarse

    def __get_data(self) -> geopandas.GeoDataFrame:
        """

        :return:
        """

        values = self.__frame
        data = geopandas.GeoDataFrame(
            values,
            geometry=geopandas.points_from_xy(values['longitude'], values['latitude'])
        )
        data.crs = 'epsg:4326'

        for field in ['maximum', 'minimum', 'latest', 'median']:
            data[field] = data[field].round(decimals=4)

        return data

    def exc(self, n_catchments_visible: int):
        """

        :param n_catchments_visible: The number of catchment data layers that are visible by default.
        :return:
        """

        coarse = self.__get_coarse_boundaries()

        __data = self.__get_data()

        limits = __data.copy()[['catchment_id', 'latest']].groupby(
            by=['catchment_id']).aggregate(lower=('latest', 'min'), upper=('latest', 'max'))

        data = __data.copy().merge(limits.reset_index(drop=False), how='left', on='catchment_id')

        src.cartography.illustrate.Illustrate(
            data=data, coarse=coarse).exc(n_catchments_visible=n_catchments_visible)
