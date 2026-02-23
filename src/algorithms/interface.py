"""Module interface.py"""

import dask
import pandas as pd

import src.algorithms.data
import src.algorithms.persist
import src.algorithms.ranking
import src.algorithms.valuations
import src.algorithms.sequences
import src.elements.partition as pr


class Interface:
    """
    The interface to quantiles calculations.
    """

    def __init__(self, listings: pd.DataFrame, arguments: dict):
        """

        :param listings: date / uri / catchment_id / ts_id
        :param arguments: A set of arguments vis-à-vis calculation & storage objectives.
        """

        self.__listings = listings
        self.__arguments = arguments

    @dask.delayed
    def __get_keys(self, ts_id: int) -> list:
        """

        :param ts_id: The identification code of a gauge's time series
        :return:
        """

        keys: pd.Series = self.__listings.loc[self.__listings['ts_id'] == ts_id, 'uri']

        return keys.to_list()

    def exc(self, partitions: list[pr.Partition], reference: pd.DataFrame) -> pd.DataFrame:
        """
        streams = src.functions.streams.Streams()
        streams.write(blob=instances, path=os.path.join(self.__configurations.data_, 'instances.csv'))

        :param partitions: The time series partitions.
        :param reference: The reference sheet of gauges.  Each instance encodes the attributes of a gauge.
        :return:
            maximum, minimum, latest, median, ending, ..., ranking
        """

        # Delayed tasks
        __data = dask.delayed(src.algorithms.data.Data(arguments=self.__arguments).exc)
        __sequences = dask.delayed(src.algorithms.sequences.Sequences(reference=reference, arguments=self.__arguments).exc)
        __valuations = dask.delayed(src.algorithms.valuations.Valuations().exc)

        # Compute
        computations = []
        for partition in partitions[:64]:
            keys = self.__get_keys(ts_id=partition.ts_id)
            data = __data(keys=keys)
            sequences = __sequences(data=data, partition=partition)
            valuations = __valuations(sequences=sequences, partition=partition)
            computations.append(valuations)
        calculations = dask.compute(computations, scheduler='threads')[0]

        # Merge each row with its descriptive attributes
        frame = pd.concat(calculations, ignore_index=True, axis=0)
        frame.dropna(axis=0, how='all', inplace=True)
        frame = frame.copy().merge(reference, how='left', on=['catchment_id', 'ts_id'])

        # Ranking
        frame = src.algorithms.ranking.Ranking().exc(frame=frame.copy())

        # Persist
        src.algorithms.persist.Persist(frame=frame).exc()

        return frame
