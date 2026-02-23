"""Module interface.py"""

import logging

import io

import boto3
import geopandas
import pandas as pd
import dask

import src.cartography.illustrate
import src.elements.s3_parameters as s3p
import src.elements.background as bck
import src.s3.unload
import src.cartography.backgrounds


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

        self.__backgrounds: list[bck.Background] = src.cartography.backgrounds.Backgrounds(connector=self.__connector)()

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

    @staticmethod
    def __get_limits(data: geopandas.GeoDataFrame):
        """

        :param data:
        :return:
        """

        limits = data.copy()[['catchment_id', 'latest']].groupby(
            by=['catchment_id']).aggregate(lower=('latest', 'min'), upper=('latest', 'max'))
        frame = data.copy().merge(limits.reset_index(drop=False), how='left', on='catchment_id')

        return frame

    def exc(self, n_catchments_visible: int):
        """

        :param n_catchments_visible: The number of catchment data layers that are visible by default.
        :return:
        """

        # Catchment boundaries
        coarse = self.__get_coarse_boundaries()

        # Metrics
        __data: geopandas.GeoDataFrame = self.__get_data()
        data = self.__get_limits(data=__data)

        # Illustrate
        __illustrate = dask.delayed(src.cartography.illustrate.Illustrate(data=data, coarse=coarse).exc)

        computations = []
        for background in self.__backgrounds:
            message = __illustrate(n_catchments_visible=n_catchments_visible, background=background)
            computations.append(message)
        messages = dask.compute(computations, scheduler='processes')
        logging.info(messages)
