import csv
import time
from io import BytesIO

import pandas as pd

from .task import task_service


class CalcService:
    def __init__(self):
        self.chunk_size = 10 ** 6

    def summa(self, task_id: str):
        # time.sleep(10)
        task = task_service.get_by_id(id=task_id)

        data = BytesIO(str.encode(task["file"]))

        # read file in chunks
        chunk = pd.read_csv(
            data,
            chunksize=self.chunk_size,
            sep=',',
            quoting=csv.QUOTE_NONE
        )

        pd_df = pd.concat(chunk)

        pd_df = self.prepare_df(pd_df=pd_df)

        cols = list(pd_df.columns.values)

        result = {}

        for i in range(10, len(cols), 10):
            summa = pd_df[list(pd_df.columns.values)[i]] \
                .astype(float).sum()
            result[str(i)] = summa

        task_service.update(id=task_id, result=result)

    def prepare_df(self, pd_df: pd.DataFrame):
        pd_df = pd_df.replace('"', '', regex=True)
        pd_df = pd_df.replace('', None)
        pd_df = pd_df.fillna(0, downcast='infer')
        return pd_df


calc_service = CalcService()
