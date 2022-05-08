import csv

import pandas as pd
from fastapi import UploadFile

from .file import file_service
from .task import task_service


class CalcService:
    def __init__(self):
        # self.chunk_size = 10 ** 6
        self.chunk_size = 10

    async def summa(self, db, upload_file: UploadFile, task_id: str):
        path_to_file = file_service.save_file(
            upload_file=upload_file,
            file_name=task_id
        )

        # read file in chunks
        chunk = pd.read_csv(
            path_to_file,
            chunksize=self.chunk_size,
            sep=',',
            quoting=csv.QUOTE_NONE
        )

        pd_df = pd.concat(chunk)

        pd_df = self.prepare_df(pd_df=pd_df)

        cols = list(pd_df.columns.values)

        result = {}

        for i in range(10, len(cols), 10):
            summa = pd_df[list(pd_df.columns.values)[i]].astype(float).sum()
            result[str(i)] = summa

        print(result)

        file_service.remove(path_to_file)

        await task_service.update(
            db=db,
            id=task_id,
            result=result
        )

    def prepare_df(self, pd_df: pd.DataFrame):
        pd_df = pd_df.replace('"', '', regex=True)
        pd_df = pd_df.replace('', None)
        pd_df = pd_df.fillna(0, downcast='infer')
        return pd_df


calc_service = CalcService()
