"""Module ranking.py"""

import pandas as pd


class Ranking:
    """
    Ranking by catchment
    """

    def __init__(self):
        pass

    @staticmethod
    def __rankings(data: pd.DataFrame) -> pd.DataFrame:
        """

        :param data:
        :return:
        """

        frame = data.copy()[['catchment_id', 'catchment_name', 'latest']].groupby(
            by=['catchment_id', 'catchment_name']).agg(metric=('latest', 'max'))

        # Convert 'catchment_id' & 'catchment_name' to fields; currently indices.
        frame.reset_index(drop=False, inplace=True)

        # Hence
        frame['rank'] = frame['metric'].rank(method='first', ascending=False).astype(int)
        frame.drop(columns='metric', inplace=True)
        frame.sort_values(by='catchment_name', inplace=True)
        frame.reset_index(drop=True, inplace=True)

        return frame

    @staticmethod
    def __drops(data: pd.DataFrame) -> pd.DataFrame:
        """
        For graphing/mapping declines in weighted rates of change

        :param data:
        :return:
        """

        frame = data.copy()[['catchment_id', 'latest']].groupby(
            by=['catchment_id']).agg(metric=('latest', 'min'))

        # Convert 'catchment_id' to a standard field; currently an index field.
        frame.reset_index(drop=False, inplace=True)

        # Hence
        frame['drop'] = frame['metric'].rank(method='first', ascending=True).astype(int)
        frame.drop(columns='metric', inplace=True)

        return frame

    def exc(self, frame: pd.DataFrame) -> pd.DataFrame:
        """

        :param frame:
        :return:
        """

        data = frame.copy()
        rankings = self.__rankings(data=data)
        drops = self.__drops(data=data)

        hence = data.merge(rankings.drop(columns=['catchment_name']), how='left', on=['catchment_id'])
        hence = hence.copy().merge(drops, how='left', on=['catchment_id'])

        return hence
