from fastapi import APIRouter, HTTPException, Depends, status, Request, Path, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session
from sqlalchemy import select, or_

from enum import Enum
from typing import Annotated, Optional

from app.models import Task
from app.backend.db_depends import get_db


router = APIRouter(
    prefix='/task',
    tags=['Tasks'],
)

DbSession = Annotated[Session, Depends(get_db)]

templates = Jinja2Templates(directory='templates')

class Priority(str, Enum):
    low = 'Низкий'
    medium = 'Средний'
    high = 'Высокий'


@router.get('/all', response_class=HTMLResponse)
async def get_all_tasks(request: Request, db: Annotated[Session, Depends(get_db)]) -> HTMLResponse:
    tasks = db.scalars(select(Task)).all()
    if len(list(tasks)) == 0:
        return templates.TemplateResponse('notfound.html', {'request': request})
    return templates.TemplateResponse('tasks.html', {'request': request, 'tasks': tasks})


@router.get('/add', response_class=HTMLResponse)
async def add_task(request: Request) -> HTMLResponse:
    return templates.TemplateResponse('add.html', {'request': request})


@router.get('/search', response_class=HTMLResponse)
async def search(request: Request, db: Annotated[Session, Depends(get_db)], query: Optional[str]):
    tasks = db.query(Task).filter(or_(Task.id.contains(query),
                                      Task.title.contains(query),
                                      Task.add_info.contains(query),
                                      Task.time.contains(query),
                                      Task.date.contains(query)))
    if len(list(tasks)) == 0:
        return templates.TemplateResponse('notfound.html', {'request': request})
    return templates.TemplateResponse('search.html', {'request': request, 'found_tasks': tasks})


@router.get('/{task_id}', response_class=HTMLResponse)
async def get_task(request: Request, task_id: Annotated[int, Path(ge=1, description='id задачи')],
                   db: Annotated[Session, Depends(get_db)]):
    """Получение информации о конкретной задаче"""
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return templates.TemplateResponse('details.html', {'request': request, 'task': task})


@router.post('/insert')
async def create_task(
                db: Annotated[Session, Depends(get_db)],
                title: str = Form(),
                priority: str = Form(),
                add_info: str = Form(),
                time_: str = Form(),
                date_: str = Form()
):
    task = Task(title=title, priority=priority, add_info=add_info, time=time_, date=date_)
    db.add(task)
    db.commit()
    return RedirectResponse(url='/task/all', status_code=status.HTTP_302_FOUND)


@router.post("/update/{task_id}")
async def update_task(db: Annotated[Session, Depends(get_db)],
                      task_id: int,
                      title: str = Form(),
                      completed: str = Form(),
                      priority: str = Form(),
                      add_info: str = Form(),
                      time_: str = Form(),
                      date_: str = Form()) -> RedirectResponse:
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    task.title = title
    task.completed = True if completed == "True" else False
    task.priority = priority
    task.add_info = add_info
    task.time = time_
    task.date = date_
    db.commit()
    return RedirectResponse(url='/task/all', status_code=status.HTTP_303_SEE_OTHER)


@router.get('/edit/{task_id}', response_class=HTMLResponse)
async def edit_task(request: Request, db: Annotated[Session, Depends(get_db)], task_id: int) -> HTMLResponse:
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return templates.TemplateResponse('update.html', {'request': request, 'task': task})


@router.get('/complete/{task_id}', response_class=HTMLResponse)
async def complete_task(db: Annotated[Session, Depends(get_db)],
                        task_id: Annotated[int, Path(ge=1, description='id задачи')],
                        ):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    task.completed = True
    print(task.completed)
    db.commit()
    return RedirectResponse(url=f'/task/edit/{task.id}', status_code=status.HTTP_302_FOUND)


@router.get('/delete/{task_id}')
async def delete_task(db: Annotated[Session, Depends(get_db)], task_id: int):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return RedirectResponse(url='/task/all', status_code=status.HTTP_302_FOUND)

