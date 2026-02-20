"""Module valuations.py"""
import numpy as np
import pandas as pd

import src.elements.partitions as pr


class Valuations:
    """
    Metrics
    """

    def __init__(self, data: pd.DataFrame, partition: pr.Partitions, arguments: dict):
        """

        :param data: Consisting of fields (a) timestamp, (b) measure
        :param partition: Refer to src.elements.partitions.py
        :param arguments:
        """

        self.__data = data.copy()
        self.__data.sort_values(by='timestamp', ascending=True, inplace=True)
        self.__partition = partition

        # time intervals (hours), and the corresponding number of points that span each time interval
        self.__tau: np.ndarray = np.array(arguments.get('tau'), dtype=float)
        self.__points: np.ndarray = (self.__tau / arguments.get('frequency')).astype(int)

    def __rates(self, i: int, j: float) -> np.ndarray:
        """

        :param i: # of points per `time interval`<br>
        :param j: time interval<br>
        :return:
        """

        # differences
        differences: np.ndarray = self.__data.copy()['measure'].diff(int(i)).values

        # 1000 * (delta measure) / (delta time); wherein 1000 converts metres to millimetres
        rates: np.ndarray = 1000 * np.true_divide(differences, j)

        return rates

    def __weights(self, i: int) -> np.ndarray:
        """

        :param i: # of points per `time interval`<br>
        :return:
            A numpy array of fractional river-level-percentage-change, with respect to different time spans
        """

        # (delta measure) / (original measure)
        weights: np.ndarray = self.__data.copy()['measure'].pct_change(int(i)).values

        return weights

    @staticmethod
    def __get_aggregates(frame: pd.DataFrame) -> pd.DataFrame:
        """

        :param frame:
        :return:
        """

        _s_max = frame['sign'].values[frame['metric'].idxmax()]
        _s_min = frame['sign'].values[frame['metric'].idxmin()]
        values = frame['sign'].values * frame['metric'].values

        aggregates = pd.DataFrame(
            data={'maximum': _s_max * frame['metric'].max(axis=0),
                  'minimum': _s_min * frame['metric'].min(axis=0),
                  'latest': values[-1:], 'median': np.nanquantile(values, q=0.5)})

        aggregates['ending'] = frame['timestamp'].max()

        return aggregates

    def __metrics(self, i: int, j: float):
        """

        :param i: # of points per `time interval`<br>
        :param j: time interval<br>
        :return:
        """

        # weights
        weights = self.__weights(i=i)

        # rates * weights, timestamps, sign
        frame = pd.DataFrame(data={'metric': self.__rates(i=i, j=j) * weights, 'timestamp': self.__data['timestamp'].values,
                                   'sign': np.where(weights < 0, -1, 1)})

        # Empty
        if frame.shape[0] == 0:
            return pd.DataFrame()

        # Metrics
        aggregates = self.__get_aggregates(frame=frame)
        aggregates = aggregates.assign(points=i)
        aggregates['catchment_id'] = self.__partition.catchment_id
        aggregates['ts_id'] = self.__partition.ts_id

        return aggregates

    def exc(self) -> pd.DataFrame:
        """

        :return:
        """

        computations = []
        for i, j in zip(self.__points, self.__tau):
            computations.append(self.__metrics(i=i, j=j))
        metrics = pd.concat(computations, axis=0)

        return metrics
