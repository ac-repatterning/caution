"""Module centroids.py"""
import typing

import geopandas


class Centroids:
    """
    Determine centroid via `epsg: 3857`, return the `epsg: 4326` form of the centroid
    """

    def __init__(self, blob: geopandas.GeoDataFrame) -> None:
        """

        :param blob:
        """

        self.__blob = blob

    def __centre(self):
        """

        :return:
        """

        dots = geopandas.GeoDataFrame({}, geometry=self.__blob.geometry)
        dots = dots.to_crs(3857)
        centre = dots.dissolve().centroid.to_crs(4326)

        return centre

    def __call__(self) -> typing.Tuple[float, float]:
        """

        :return:
        """

        centre = self.__centre()
        c_latitude = float(centre.geometry.apply(lambda c: c.y)[0])
        c_longitude = float(centre.geometry.apply(lambda c: c.x)[0])

        return c_latitude, c_longitude
