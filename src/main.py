from fastapi import FastAPI
from views.thumbnail import Thumbnail
import uvicorn
import os
import logging
import sys


logging.basicConfig(
    level=logging.DEBUG,
    format="[%(name)s] %(levelname)s: [%(filename)s:%(funcName)s] %(message)s",
    datefmt="%d/%m/%Y %H.%M.%S",
    stream=sys.stdout,
)


os.environ["PYPPETEER_CHROMIUM_REVISION"] = "1263111"

app = FastAPI()
app.include_router(Thumbnail().router)