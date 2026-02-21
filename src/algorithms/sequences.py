"""Modules sequences.py"""
import numpy as np
import pandas as pd


class Sequences:
    """

    Sequences
    """

    def __init__(self, arguments: dict):
        """

        :param arguments:
        """

        # time intervals (hours), and the corresponding number of points that span each time interval
        self.__tau: float  = float(arguments.get('tau'))
        self.__points: int = int(self.__tau / float(arguments.get('frequency')))

    def __rates(self, data: pd.DataFrame) -> np.ndarray:
        """

        :param data: data<br>
        :return:
        """

        # differences
        differences: np.ndarray = data.copy()['measure'].diff(self.__points).values

        # 1000 * (delta measure) / (delta time); wherein 1000 converts metres to millimetres
        rates: np.ndarray = 1000 * np.true_divide(differences, self.__tau)

        return rates

    def __weights(self, data: pd.DataFrame) -> np.ndarray:
        """

        :param data: data<br>
        :return:
            A numpy array of fractional river-level-percentage-change, with respect to different time spans
        """

        # (delta measure) / (original measure)
        weights: np.ndarray = data.copy()['measure'].pct_change(self.__points).values

        return weights

    def exc(self, data: pd.DataFrame) -> pd.DataFrame:
        """

        :param data: Consisting of fields (a) timestamp, (b) measure
        :return:
        """

        if data.empty:
            return pd.DataFrame()

        __data = data.copy()
        __data.sort_values(by='timestamp', ascending=True, inplace=True)
        weights = self.__weights(data=__data.copy())
        rates = self.__rates(data=__data.copy())

        # rates * weights, timestamps, sign
        values = pd.DataFrame(
            data={'metric': rates * weights, 'timestamp': __data['timestamp'].values,
                  'sign': np.where(weights < 0, -1, 1)})
        values = values.assign(approximation=values['sign'] * values['metric'])

        return values
