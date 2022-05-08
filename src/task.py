from fastapi.encoders import jsonable_encoder

from . import schemas
from .constants import DONE_STATUS


class TaskService:
    def __init__(self):
        self.collection = "task"

    async def create(self, db) -> schemas.Task:
        new_task = await db[self.collection].insert_one(
            jsonable_encoder(schemas.TaskCreate())
        )

        task_in_db = await db[self.collection].find_one({"_id": new_task.inserted_id})

        return schemas.Task(**task_in_db)

    async def update(self, db, id: str, result: dict) -> None:
        obj_in = schemas.TaskUpdate(
            result=result,
            status=DONE_STATUS
        )

        await db[self.collection].update_one(
            {"_id": id},
            {"$set": jsonable_encoder(obj_in)}
        )


task_service = TaskService()
