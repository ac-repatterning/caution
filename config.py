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
        self.caution_ = os.path.join(self.warehouse, 'caution')
        self.points_ = os.path.join(self.caution_, 'points')
        self.menu_ = os.path.join(self.caution_, 'menu')
        self.maps_ = os.path.join(self.caution_, 'maps')
        self.series_ = os.path.join(self.caution_, 'series')

        # Template
        self.s3_parameters_key = 's3_parameters.yaml'
        self.arguments_key = 'caution/arguments.json'
        self.metadata_key = 'caution/external/metadata.json'

        # The storage prefix
        self.prefix = 'warehouse/caution'

        # Project metadata
        self.project_tag = 'hydrography'
        self.project_key_name = 'HydrographyProject'
