"""Modules sequences.py"""
import logging
import os

import numpy as np
import pandas as pd

import json

import config
import src.elements.partitions as pr
import src.functions.objects


class Sequences:
    """

    Sequences
    """

    def __init__(self, reference: pd.DataFrame, arguments: dict):
        """

        :param reference:
        :param arguments:
        """

        self.__reference = reference

        self.__configurations = config.Config()
        self.__objects = src.functions.objects.Objects()

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

    def __persist(self, values: pd.DataFrame, partition: pr.Partitions) -> str:
        """

        :param values:
        :param partition:
        :return:
        """

        attributes: pd.Series = self.__reference.loc[self.__reference['ts_id'] == partition.ts_id, :][0]
        logging.info('ATTRIBUTES:\n%s', attributes)

        string = values.to_json(orient='split')
        nodes: dict = json.loads(string)
        nodes.update(attributes.to_dict())

        return self.__objects.write(
            nodes=nodes, path=os.path.join(self.__configurations.series_, f'{partition.ts_id}.json'))

    def exc(self, data: pd.DataFrame, partition: pr.Partitions) -> pd.DataFrame:
        """

        :param data: Consisting of fields (a) timestamp, (b) measure
        :param partition:
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

        # Persist
        self.__persist(values=values, partition=partition)

        return values
