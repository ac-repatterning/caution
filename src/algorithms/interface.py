"""Module interface.py"""

import dask
import pandas as pd

import src.algorithms.data
import src.algorithms.persist
import src.algorithms.ranking
import src.algorithms.valuations
import src.elements.partitions as pr


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

    @dask.delayed
    def __get_metrics(self, data: pd.DataFrame, partition: pr.Partitions):
        """

        :param data:
        :param partition:
        :return:
        """

        return src.algorithms.valuations.Valuations(
            data=data, partition=partition, arguments=self.__arguments).exc()

    def exc(self, partitions: list[pr.Partitions], reference: pd.DataFrame) -> pd.DataFrame:
        """
        streams = src.functions.streams.Streams()
        streams.write(blob=instances, path=os.path.join(self.__configurations.data_, 'instances.csv'))

        :param partitions: The time series partitions.
        :param reference: The reference sheet of gauges.  Each instance encodes the attributes of a gauge.
        :return:
        """

        reference.info()

        # Delayed tasks
        __data = dask.delayed(src.algorithms.data.Data(arguments=self.__arguments).exc)

        # Compute
        computations = []
        for partition in partitions:
            keys = self.__get_keys(ts_id=partition.ts_id)
            data = __data(keys=keys)
            metrics = self.__get_metrics(data=data, partition=partition)
            computations.append(metrics)
        calculations = dask.compute(computations, scheduler='threads')[0]

        # Merge each instance with its descriptive attributes
        instances = pd.concat(calculations, ignore_index=True, axis=0)
        instances = instances.copy().merge(reference, how='left', on=['catchment_id', 'ts_id'])
        instances['hours'] = self.__arguments.get('frequency') * instances['points']

        # Ranking
        instances = src.algorithms.ranking.Ranking().exc(instances=instances.copy())

        # Persist
        src.algorithms.persist.Persist(instances=instances).exc()

        return instances
