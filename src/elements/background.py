"""Module background.py"""
import typing


class Background(typing.NamedTuple):
    """
    The data type class ⇾ Background<br><br>

    Attributes<br>
    ----------<br>
    <b>tiles</b>: str<br>
        The tiles.<br><br>
    <b>filename</b>: str<br>
        The file name of a map.<br><br>
    <b>zoom_start</b>: int<br>
        Zoom start.<br><br>
    <b>min_zoom</b>: int<br>
        Minimum zoom.<br><br>
    <b>max_zoom</b>: int<br>
        Maximum zoom.<br><br>
    <b>crs</b>: str<br>
        Coördinate reference system string; format EPSG:0000<br><br>
    <b>attr</b>: str<br>
        Attribution.<br><br>
    """

    tiles: str
    filename: str
    zoom_start: int
    min_zoom: int
    max_zoom: int
    crs: str
    attr: str = None
