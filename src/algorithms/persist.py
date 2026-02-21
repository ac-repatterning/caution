"""Module persist.py"""
import logging
import os

import pandas as pd

import config
import src.algorithms.disaggregates
import src.functions.directories
import src.functions.objects


class Persist:
    """
    Persist
    """

    def __init__(self, frame: pd.DataFrame):
        """

        :param frame:
        """

        self.__frame = frame

        # Names
        self.__names: dict = {-1: 'negative', 1: 'positive'}

        # Instances
        self.__configurations = config.Config()
        self.__objects = src.functions.objects.Objects()

    def __get_nodes(self, sign: int) -> dict | list[dict]:
        """

        :param sign: {-1, +1}
        :return:
        """

        frame: pd.DataFrame = self.__frame.copy().loc[self.__frame['sign'] == sign, :]
        nodes = src.algorithms.disaggregates.Disaggregates(frame=frame)()

        return nodes

    def __persist(self, nodes: dict| list[dict], sign: int):
        """

        :param nodes:
        :param sign:
        :return:
        """

        return self.__objects.write(
            nodes=nodes, path=os.path.join(self.__configurations.points_, f'{self.__names.get(sign)}.json'))

    def exc(self):
        """

        :return:
        """

        # Negatives & Positives
        computations = []
        for sign in self.__names.keys():
            nodes = self.__get_nodes(sign=sign)
            message = self.__persist(nodes=nodes, sign=sign)
            computations.append(message)
        logging.info(computations)
