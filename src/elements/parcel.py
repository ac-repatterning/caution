"""Module priorities.py"""
import typing


class Parcel(typing.NamedTuple):
    """
    The data type class ⇾ Priorities<br><br>

    Attributes<br>
    ----------<br>
    <b>rank</b>: int<br>
        A catchment's rank in relation its maximum millimetres/hour value; the catchment that has
        the highest maximum value has rank 0 or 1.<br><br>
    <b>catchment_id</b>: int<br>
        The identification code of a catchment area.<br><br>
    <b>catchment_name</b>: str<br>
        The corresponding catchment name.<br><br>
    <b>decimal</b>: float<br>
        A decimal number for colour coding.<br><br>
    """

    rank: int
    catchment_id: int
    catchment_name: str
    decimal: float
