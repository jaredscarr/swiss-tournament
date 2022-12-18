from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.api.api_v1.api import api_router

import os

stage = os.environ.get('STAGE', None)
root_path = f'/{stage}' if stage else '/'
app = FastAPI(title='Swiss Tournament', root_path=root_path)
app.include_router(api_router, prefix='/api/v1')
origins = settings.CORS_ORIGINS.split(',')

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.get('/')
def read_root():
    return {'message': 'Hello World'}
