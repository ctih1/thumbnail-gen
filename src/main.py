from fastapi import FastAPI
from .views.thumbnail import Thumbnail
import uvicorn
import logging
import sys
import os


logging.basicConfig(
    level=logging.DEBUG,
    format="[%(name)s] %(levelname)s: [%(filename)s:%(funcName)s] %(message)s",
    datefmt="%d/%m/%Y %H.%M.%S",
    stream=sys.stdout,
)


app = FastAPI()
app.include_router(Thumbnail().router)