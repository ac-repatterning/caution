"""Module partition.py"""
import typing


class Partition(typing.NamedTuple):
    """
    The data type class ⇾ Partitions<br><br>

    Attributes<br>
    ----------<br>
    <b>catchment_id</b>: int<br>
        The identification code of a catchment area.<br><br>
    <b>ts_id</b>: int<br>
        The identification code of a time series.<br><br>
    """

    catchment_id: int
    ts_id: int
