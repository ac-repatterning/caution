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
            by=['catchment_id', 'catchment_name']).agg(maximum=('latest', 'max'))

        # Convert 'catchment_id' & 'catchment_name' to fields; currently indices.
        frame.reset_index(drop=False, inplace=True)

        # Hence
        frame['rank'] = frame['maximum'].rank(method='first', ascending=False).astype(int)
        frame.drop(columns='maximum', inplace=True)
        frame.sort_values(by='catchment_name', inplace=True)
        frame.reset_index(drop=True, inplace=True)

        return frame

    def exc(self, frame: pd.DataFrame) -> pd.DataFrame:
        """

        :param frame:
        :return:
        """

        data = frame.copy()
        rankings = self.__rankings(data=data)
        hence = data.merge(rankings.drop(columns=['catchment_name']), how='left', on=['catchment_id'])

        return hence
