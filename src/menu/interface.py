"""Module interface.py"""
import logging
import os

import numpy as np
import pandas as pd

import config
import src.functions.objects


class Interface:
    """
    Menu
    """

    def __init__(self):
        """
        Constructor
        """

        self.__configurations = config.Config()
        self.__objects = src.functions.objects.Objects()

    def __menu(self, frame: pd.DataFrame):
        """

        :param frame:
        :return:
        """

        nodes = frame.to_dict(orient='records')

        return self.__objects.write(
            nodes=nodes, path=os.path.join(self.__configurations.menu_, 'menu.json'))


    def exc(self, points_: np.ndarray, frequency: float):
        """

        :param points_:
        :param frequency:
        :return:
        """

        # Menu codes
        codes = [f'{p:04d}' for p in points_]

        # Menu Names
        hours = frequency * points_
        names = [f'{h} hours' if h != 1 else f'{int(h)} hour' for h in hours ]

        # Build the menu
        frame = pd.DataFrame(data={'desc': codes, 'name': names})
        message = self.__menu(frame=frame)

        logging.info('Menu ->\n%s', message)
