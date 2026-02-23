"""Module illustrate.py"""
import os

import folium
import folium.plugins
import geopandas

import config
import src.cartography.centroids
import src.cartography.custom
import src.cartography.metadata
import src.cartography.parcels
import src.elements.background as bck
import src.elements.parcel as pcl


class Illustrate:
    """
    Illustrate
    """

    def __init__(self, data: geopandas.GeoDataFrame, coarse: geopandas.GeoDataFrame):
        """

        :param data: The frame of metrics per gauge station.
        :param coarse: The overarching catchments
        """

        self.__data = data
        self.__coarse = coarse

        # Configurations
        self.__configurations = config.Config()

        # Metadata: Gauge Station
        self.__metadata = src.cartography.metadata.Metadata()

        # Centroid, Parcels
        self.__c_latitude, self.__c_longitude = src.cartography.centroids.Centroids(blob=self.__data).__call__()
        self.__parcels: list[pcl.Parcel] = src.cartography.parcels.Parcels(data=self.__data).exc()

    def exc(self, n_catchments_visible: int, background: bck.Background) -> str:
        """

        :param n_catchments_visible: The number of catchment data layers that are visible by default.
        :param background: Refer to src/elements/background.py
        :return:
        """

        # Custom drawing functions
        custom = src.cartography.custom.Custom()

        # Base Layer: TileLayer objects aid the security of map service details.
        segments = folium.Map(location=[self.__c_latitude, self.__c_longitude],
                              tiles=folium.raster_layers.TileLayer(
                                  tiles=background.tiles, name=background.filename, attr=background.attr),
                              attr=background.attr,
                              zoom_start=background.zoom_start, min_zoom=background.min_zoom, max_zoom=background.max_zoom,
                              crs=background.crs, max_bounds=True)

        # Uncontrollable Layer
        folium.GeoJson(
            data=self.__coarse.to_crs(epsg=3857),
            name='Boundaries',
            style_function=lambda feature: {
                "fillColor": "#ffffff", "color": "black", "opacity": 0.35, "weight": 0.85, "dashArray": "5, 2"
            },
            tooltip=folium.GeoJsonTooltip(fields=["catchment_name"], aliases=["Catchment Name"]),
            control=False,
            highlight_function=lambda feature: {
                "fillColor": "#6b8e23", "fillOpacity": 0.1
            }
        ).add_to(segments)

        # Gauge Stations by Catchment
        for parcel in self.__parcels:

            show = parcel.rank < n_catchments_visible

            # The instances of a catchment
            instances = self.__data.copy().loc[self.__data['catchment_id'] == parcel.catchment_id, :]

            # Draw
            on_each_feature = folium.utilities.JsCode(self.__metadata())
            folium.GeoJson(
                data = instances.to_crs(epsg=3857),
                name=f'{parcel.catchment_name}',
                marker=folium.CircleMarker(
                    radius=27.5, weight=4, stroke=False, fill=True),
                style_function=lambda feature: {
                    "fillOpacity": custom.f_opacity(feature['properties']['latest'],
                                                    lower=feature['properties']['lower'],
                                                    upper=feature['properties']['upper']),
                    "fillColor": custom.f_fill_colour(feature['properties']['latest']),
                    "radius": custom.f_radius(feature['properties']['latest'])
                },
                zoom_on_click=True,
                on_each_feature=on_each_feature,
                show=show
            ).add_to(segments)

        folium.LayerControl().add_to(segments)

        # Drawing Tool
        folium.plugins.Draw(
            export=False, position='bottomleft', show_geometry_on_click=False,
            draw_options={'polyline': False, 'polygon': False, 'rectangle': False, 'marker': False,
                          'circle': {'shapeOptions': {'color': '#6495ed', 'stroke': True, 'dashArray': '', 'opacity': 0.35}},
                          'circlemarker': {'color': '#000000', 'opacity': 0.85, 'fillOpacity': 0.35}}
        ).add_to(segments)

        # Persist
        outfile = os.path.join(self.__configurations.maps_, f'{background.filename}.html')
        segments.save(outfile=outfile)

        return f'{background.filename}.html'
