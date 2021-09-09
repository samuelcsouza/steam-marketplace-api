import importlib

from fastapi import FastAPI
from src.services.crawler import Crawler

app = FastAPI()

instance = Crawler()

api_module = importlib.import_module("src.routers.api")

app.include_router(api_module.api_router)
