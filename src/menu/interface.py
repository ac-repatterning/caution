"""Module interface.py"""
import logging
import os
import glob

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


    def exc(self, reference: pd.DataFrame):
        """

        :param reference:
        :return:
        """

        listing = glob.glob(os.path.join(self.__configurations.series_, '*.json'))
        logging.info(listing)


