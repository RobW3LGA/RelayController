import uvicorn
from fastapi import FastAPI, APIRouter

from pathlib import Path

from models import DeviceSource, TaskSource
from settings import apiServiceParam
from utilities import getDataSource, isAuthenticated
from components import invokeApiRoutes


apiService: FastAPI = FastAPI(

  docs_url=apiServiceParam["docs_url"],
  redoc_url=apiServiceParam["redoc_url"]
)

apiRouter: APIRouter = APIRouter()

invokeApiRoutes(
  apiRouter=apiRouter,
  deviceSource=getDataSource(path=apiServiceParam["device_db"], source=DeviceSource),
  taskSource=getDataSource(path=apiServiceParam["task_db"], source=TaskSource),
  isAuthenticated=isAuthenticated
)

apiService.include_router(router=apiRouter, prefix=apiServiceParam["prefix"])


if __name__ == "__main__":

  uvicorn.run(

    app="main:apiService",
    host=apiServiceParam["allhosts"],
    port=apiServiceParam["port"],
    ssl_keyfile=Path(apiServiceParam["ssl_keyfile"]),
    ssl_certfile=Path(apiServiceParam["ssl_certfile"]),
    lifespan=apiServiceParam["lifespan"],
    log_level=apiServiceParam["log_level"]
  )
