"""
Module config
"""
import os


class Config:
    """
    Class Config

    For project settings
    """

    def __init__(self):
        """
        Constructor
        """

        self.warehouse: str = os.path.join(os.getcwd(), 'warehouse')
        self.risks_ = os.path.join(self.warehouse, 'risks')
        self.points_ = os.path.join(self.risks_, 'points')
        self.menu_ = os.path.join(self.risks_, 'menu')
        self.maps_ = os.path.join(self.risks_, 'maps')

        # Template
        self.s3_parameters_key = 's3_parameters.yaml'
        self.arguments_key = 'risks/arguments.json'
        self.metadata_ = 'risks/external'

        # The storage prefix
        self.prefix = 'warehouse/risks'
