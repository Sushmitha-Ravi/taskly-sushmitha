import json
import logging
import time
import uuid
from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import Response
from pydantic import BaseModel
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    Counter,
    Histogram,
    generate_latest,
)
from sqlalchemy.orm import Session

from database import SessionLocal, create_tables
from logging_config import configure_logging
from models import TaskModel
from redis_client import redis_client


app = FastAPI(
    title="Tasks API",
    description="Bootcamp demo app — Week 1/2/8",
)


configure_logging()

logger = logging.getLogger("taskly")

create_tables()


# -------------------------
# Prometheus metrics
# -------------------------

http_requests_total = Counter(
    "taskly_http_requests_total",
    "Total number of HTTP requests",
    ["method", "path", "status"],
)

http_request_duration_seconds = Histogram(
    "taskly_http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "path"],
)

tasks_created_total = Counter(
    "tasks_created_total",
    "Total number of tasks created",
)


# -------------------------
# Database dependency
# -------------------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------
# Request metrics middleware
# -------------------------

@app.middleware("http")
async def metrics_middleware(request, call_next):
    start_time = time.perf_counter()

    response = await call_next(request)

    duration = time.perf_counter() - start_time

    http_requests_total.labels(
        method=request.method,
        path=request.url.path,
        status=str(response.status_code),
    ).inc()

    http_request_duration_seconds.labels(
        method=request.method,
        path=request.url.path,
    ).observe(duration)

    return response

@app.middleware("http")
async def request_id_middleware(request, call_next):
    request_id = str(uuid.uuid4())

    request.state.request_id = request_id

    response = await call_next(request)

    response.headers["X-Request-ID"] = request_id

    return response



# -------------------------
# Pydantic models
# -------------------------

class Task(BaseModel):
    title: str
    description: Optional[str] = None
    done: bool = False
    priority: Optional[str] = None


class TaskOut(Task):
    id: int


# -------------------------
# Health
# -------------------------

@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "tasks-api",
    }


# -------------------------
# Prometheus metrics
# -------------------------

@app.get("/metrics")
def metrics():
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )


# -------------------------
# List tasks
# -------------------------

@app.get("/tasks", response_model=List[TaskOut])
def list_tasks(db: Session = Depends(get_db)):
    cached_tasks = redis_client.get("tasks:all")

    if cached_tasks:
        return json.loads(cached_tasks)

    tasks = db.query(TaskModel).all()

    result = [
        {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "done": task.done,
            "priority": task.priority,
        }
        for task in tasks
    ]

    redis_client.set(
        "tasks:all",
        json.dumps(result),
        ex=60,
    )

    return result


# -------------------------
# Create task
# -------------------------

@app.post("/tasks", response_model=TaskOut, status_code=201)
def create_task(
    request: Request,
    task: Task,
    db: Session = Depends(get_db),
):
    db_task = TaskModel(
        title=task.title,
        description=task.description,
        done=task.done,
        priority=task.priority,
    )

    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    tasks_created_total.inc()

    logger.info(
        "Task created",
        extra={
            "task_id": db_task.id,
            "request_id": request.state.request_id,
        },
    )

    redis_client.delete("tasks:all")

    return {
        "id": db_task.id,
        "title": db_task.title,
        "description": db_task.description,
        "done": db_task.done,
        "priority": db_task.priority,
    }


# -------------------------
# Get one task
# -------------------------

@app.get("/tasks/{task_id}", response_model=TaskOut)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
):
    task = (
        db.query(TaskModel)
        .filter(TaskModel.id == task_id)
        .first()
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "done": task.done,
        "priority": task.priority,
    }


# -------------------------
# Update task
# -------------------------

@app.patch("/tasks/{task_id}", response_model=TaskOut)
def update_task(
    task_id: int,
    task: Task,
    db: Session = Depends(get_db),
):
    db_task = (
        db.query(TaskModel)
        .filter(TaskModel.id == task_id)
        .first()
    )

    if db_task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    db_task.title = task.title
    db_task.description = task.description
    db_task.done = task.done
    db_task.priority = task.priority

    db.commit()
    db.refresh(db_task)

    redis_client.delete("tasks:all")

    return {
        "id": db_task.id,
        "title": db_task.title,
        "description": db_task.description,
        "done": db_task.done,
        "priority": db_task.priority,
    }


# -------------------------
# Delete task
# -------------------------

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
):
    db_task = (
        db.query(TaskModel)
        .filter(TaskModel.id == task_id)
        .first()
    )

    if db_task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    db.delete(db_task)
    db.commit()

    redis_client.delete("tasks:all")