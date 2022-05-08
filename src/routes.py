from fastapi import APIRouter, Depends, File, UploadFile, BackgroundTasks

from .calc import calc_service
from .db.session import get_db
from .schemas import Task
from .task import task_service

router = APIRouter()


@router.get('/', tags=['Root'])
async def root():
    return {'message': '200 OK'}


@router.post(
    '/task',
    response_model=Task,
    response_model_exclude_none=True,
)
async def create(
        *, db=Depends(get_db),
        file: UploadFile = File(...),
        background_tasks: BackgroundTasks
):
    task = await task_service.create(db=db)
    background_tasks.add_task(
        calc_service.summa,
        db=db,
        upload_file=file,
        task_id=str(task.id)
    )
    # await calc_service.summa(db=db, upload_file=file, task_id=str(task.id))
    return task
