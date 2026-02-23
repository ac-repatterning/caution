"""Module valuations.py"""
import numpy as np
import pandas as pd

import src.elements.partition as pr


class Valuations:
    """
    Metrics
    """

    def __init__(self):
        pass

    @staticmethod
    def __get_aggregates(sequences: pd.DataFrame) -> pd.DataFrame:
        """

        :param sequences:
        :return:
        """

        _s_max = sequences['sign'].values[sequences['metric'].idxmax()]
        _s_min = sequences['sign'].values[sequences['metric'].idxmin()]

        aggregates = pd.DataFrame(
            data={'maximum': _s_max * sequences['metric'].max(axis=0),
                  'minimum': _s_min * sequences['metric'].min(axis=0),
                  'latest': sequences['approximation'].values[-1:],
                  'direction': sequences['sign'].values[-1:],
                  'median': np.nanquantile(sequences['approximation'].values, q=0.5)})

        aggregates['p_ending'] = sequences['timestamp'].max()
        aggregates['p_beginning'] = sequences['timestamp'].min()

        return aggregates

    def exc(self, sequences: pd.DataFrame, partition: pr.Partition) -> pd.DataFrame:
        """

        :param sequences: metric, timestamp, sign, approximation -> whereby approximation = sign * metric
        :param partition: Refer to ...
        :return:
        """

        if sequences.empty:
            return pd.DataFrame()

        aggregates = self.__get_aggregates(sequences=sequences)
        aggregates['catchment_id'] = partition.catchment_id
        aggregates['ts_id'] = partition.ts_id

        return aggregates
