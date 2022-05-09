from typing import List

from fastapi import UploadFile
from fastapi.encoders import jsonable_encoder

from . import schemas
from .constants import DONE_STATUS
from .db.session import get_db


class TaskService:
    def __init__(self):
        self.collection = "task"

    def create(self, upload_file: UploadFile) -> schemas.Task:
        db = get_db()

        file_bytes = upload_file.file.read()

        new_task = db[self.collection].insert_one(
            jsonable_encoder(schemas.TaskCreate(file=file_bytes))
        )

        task_in_db = db[self.collection].find_one({"_id": new_task.inserted_id})

        return schemas.Task(**task_in_db)

    def update(self, id: str, result: dict, file: bytes = None) -> None:
        db = get_db()

        obj_in = schemas.TaskUpdate(
            result=result,
            status=DONE_STATUS,
            file=file
        )

        db[self.collection].update_one(
            {"_id": id},
            {"$set": jsonable_encoder(obj_in)}
        )

    def find(self, status: str = None) -> List[schemas.Task]:
        db = get_db()

        params = {}

        if status is not None:
            params["status"] = status

        tasks = list(db[self.collection].find(params))

        return tasks

    def get_by_id(self, id: str = None):
        db = get_db()
        return db[self.collection].find_one({"_id": id})


task_service = TaskService()
