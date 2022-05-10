from typing import List

from fastapi import APIRouter, File, UploadFile, HTTPException, status

from .constants import IN_PROGRESS_STATUS
from .schemas import Task
from .task import task_service
from .worker import create_task

router = APIRouter()


@router.get('/', tags=['Root'])
async def root():
    return {'message': '200 OK'}


@router.post(
    '/task',
    tags=['Task'],
    response_model=Task,
    response_model_exclude_none=True
)
def create(file: UploadFile = File(...)):
    task = task_service.create(upload_file=file)

    task_ = create_task.delay(str(task.id))

    print(task_.id)

    return task


@router.get(
    '/task',
    tags=['Task'],
    response_model=Task,
    response_model_exclude_none=True,
    responses={
        404: {"description": "Not found"}
    },
    summary="Find task by id"
)
def get_by_id(id: str):
    task = task_service.get_by_id(id=id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task


@router.get(
    '/task/run',
    tags=['Task'],
    response_model=List[Task],
    response_model_exclude_none=True,
    summary="Find running tasks"
)
def find_run():
    return task_service.find(status=IN_PROGRESS_STATUS)
