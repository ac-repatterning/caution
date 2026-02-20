"""Module parcels.py"""
import geopandas
import numpy as np

import src.elements.parcel as pcl


class Parcels:
    """
    Parcels
    """

    def __init__(self, data: geopandas.GeoDataFrame):
        """

        :param data: The frame of metrics per gauge station.
        """

        self.__data = data

        # Seed
        self.__seed = 5

    def __get_decimals(self, size: int):
        """

        :param size: The number of required random numbers
        :return:
        """

        rng = np.random.default_rng(seed=self.__seed)

        return rng.uniform(low=0.25, high=0.90, size=size)

    def exc(self) -> list[pcl.Parcel]:
        """

        :return:
        """

        catchments = self.__data.copy()[['catchment_id', 'catchment_name', 'rank']].drop_duplicates()
        catchments.sort_values(by='catchment_name', inplace=True)
        catchments['decimal'] = self.__get_decimals(size=catchments.shape[0])

        # An iterable for mapping by layer
        values: list[dict] = catchments.to_dict(orient='records')
        parcels = [pcl.Parcel(**value) for value in values]

        return parcels
