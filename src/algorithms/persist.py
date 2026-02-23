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

    def __get_nodes(self, direction: int) -> dict | list[dict]:
        """

        :param direction: {-1, +1}
        :return:
        """

        frame: pd.DataFrame = self.__frame.copy().loc[self.__frame['direction'] == direction, :]
        if frame.empty:
            return {}

        nodes = src.algorithms.disaggregates.Disaggregates(frame=frame)()

        return nodes

    def __persist(self, nodes: dict| list[dict], direction: int):
        """

        :param nodes:
        :param direction:
        :return:
        """

        if not nodes:
            return f'{self.__names.get('direction')}: empty'

        return self.__objects.write(
            nodes=nodes, path=os.path.join(self.__configurations.points_, f'{self.__names.get(direction)}.json'))

    def exc(self):
        """

        :return:
        """

        # Negatives & Positives
        computations = []
        for direction, _ in self.__names.items():
            nodes = self.__get_nodes(direction=direction)
            message = self.__persist(nodes=nodes, direction=direction)
            computations.append(message)
        logging.info(computations)
