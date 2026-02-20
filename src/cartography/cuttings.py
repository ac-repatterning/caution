"""Module cuttings.py"""
import geopandas
import shapely


class Cuttings:
    """
    Intersections of polygons
    """

    def __init__(self, instances: geopandas.GeoDataFrame):
        """

        instances: the geometry field of `instances` encodes the points from a single/distinct parent catchment
        """

        self.__instances = instances

    def inside(self, _polygon: shapely.geometry.polygon.Polygon):
        """

        :param _polygon:
        :return:
        """

        # Is y a member of polygon `_polygon`? `y` is a geometry point of self.__instances
        outputs = self.__instances.geometry.apply(lambda y: y.within(_polygon))

        return sum(outputs)
