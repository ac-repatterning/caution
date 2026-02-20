"""Module main.py"""
import datetime
import logging
import os
import sys

import boto3


def main():
    """

    :return:
    """

    logger: logging.Logger = logging.getLogger(__name__)
    logger.info('Starting: %s', datetime.datetime.now().isoformat(timespec='microseconds'))

    # The time series partitions, the reference sheet of gauges
    partitions, listings, reference = src.assets.interface.Interface(
        service=service, s3_parameters=s3_parameters, arguments=arguments).exc()

    # Hence
    instances = src.algorithms.interface.Interface(listings=listings, arguments=arguments).exc(
        partitions=partitions, reference=reference)
    instances.info()

    src.cartography.interface.Interface(
        connector=connector, s3_parameters=s3_parameters, instances=instances).exc(
        n_catchments_visible=arguments.get('rates').get('n_catchments_visible'))

    src.menu.interface.Interface().exc(
        points_=instances['points'].unique(), frequency=arguments.get('frequency'))

    # Transferring calculations to an Amazon S3 (Simple Storage Service) bucket
    src.transfer.interface.Interface(
        connector=connector, service=service, s3_parameters=s3_parameters).exc()

    # Cache
    src.functions.cache.Cache().exc()


if __name__ == '__main__':

    root = os.getcwd()
    sys.path.append(root)
    sys.path.append(os.path.join(root, 'src'))

    # Logging
    logging.basicConfig(level=logging.INFO,
                        format='\n\n%(message)s\n%(asctime)s.%(msecs)03d\n',
                        datefmt='%Y-%m-%d %H:%M:%S')

    # Modules
    import src.assets.interface
    import src.algorithms.interface
    import src.cartography.interface
    import src.elements.s3_parameters as s3p
    import src.elements.service as sr
    import src.functions.cache
    import src.menu.interface
    import src.preface.interface
    import src.transfer.interface

    connector: boto3.session.Session
    s3_parameters: s3p.S3Parameters
    service: sr.Service
    arguments: dict
    connector, s3_parameters, service, arguments = src.preface.interface.Interface().exc()

    main()
