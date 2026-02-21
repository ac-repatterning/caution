"""Module illustrate.py"""
import os

import folium
import geopandas

import config
import src.cartography.centroids
import src.cartography.custom
import src.cartography.parcels
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

        # Centroid, Parcels
        self.__c_latitude, self.__c_longitude = src.cartography.centroids.Centroids(blob=self.__data).__call__()
        self.__parcels: list[pcl.Parcel] = src.cartography.parcels.Parcels(data=self.__data).exc()

    def exc(self, n_catchments_visible: int):
        """
        popup=folium.GeoJsonPopup(fields=['station_name', 'latest', 'maximum', 'median'],
                                  aliases=['Station Name', 'latest (mm/hr)', 'maximum (mm/hr)', 'median (mm/hr)'])

        :param n_catchments_visible: The number of catchment data layers that are visible by default.
        :return:
        """

        # Colours
        # colours: branca.colormap.StepColormap = branca.colormap.LinearColormap(
        #     ['black', 'brown', 'orange']).to_step(len(self.__parcels))

        # Custom drawing functions
        custom = src.cartography.custom.Custom()

        # Base Layer
        segments = folium.Map(location=[self.__c_latitude, self.__c_longitude], tiles='OpenStreetMap', zoom_start=7)

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
            folium.GeoJson(
                data = instances.to_crs(epsg=3857),
                name=f'{parcel.catchment_name}',
                marker=folium.CircleMarker(
                    radius=27.5, weight=4, stroke=False, fill=True),
                tooltip=folium.GeoJsonTooltip(
                    fields=['latest', 'maximum', 'median', 'station_name', 'river_name', 'catchment_name'],
                    aliases=['latest (mm/hr)', 'maximum (mm/hr)', 'median (mm/hr)', 'Station', 'River/Water', 'Catchment']),
                style_function=lambda feature: {
                    "fillOpacity": custom.f_opacity(feature['properties']['latest'],
                                                    lower=feature['properties']['lower'],
                                                    upper=feature['properties']['upper']),
                    "fillColor": custom.f_fill_colour(feature['properties']['latest']),
                    "radius": custom.f_radius(feature['properties']['latest'])
                },
                zoom_on_click=True,
                show=show
            ).add_to(segments)

        folium.LayerControl().add_to(segments)

        # Persist
        outfile = os.path.join(self.__configurations.maps_, 'map.html')
        segments.save(outfile=outfile)
