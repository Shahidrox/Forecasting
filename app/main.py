from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from fastapi.staticfiles import StaticFiles

from src.core import config
from src.routes import api_router
from src.services import seed_service

from src.utils.logger_utils import logger
"""
This script initializes a FastAPI application for forecasting.
The script performs the following steps:
1. Imports necessary modules and packages.
2. Defines an async context manager `lifespan` that runs the `run_seed` function before yielding.
3. Defines the `run_seed` function that logs a message and creates a seed.
4. Creates a FastAPI application object with the `lifespan` parameter set to the `lifespan` async context manager and the `title` parameter set to 'Forecasting'.
5. Mounts a static directory for the admin interface.
6. Sets the allowed origins for CORS (Cross-Origin Resource Sharing) based on the `BACKEND_CORS_ORIGINS` configuration.
7. Includes the API router in the application.
Note: This script assumes the existence of the following modules/packages:
- `fastapi` for creating the FastAPI application.
- `starlette.middleware.cors` for enabling CORS middleware.
- `contextlib` for defining async context managers.
- `fastapi.staticfiles` for serving static files.
- `src.core.config` for accessing configuration settings.
- `src.routes.api_router` for including the API router.
- `src.services.seed_service` for creating a seed.
- `src.utils.logger_utils` for logging messages.
"""

@asynccontextmanager
async def lifespan(app: FastAPI):
  try:
    run_seed()
    yield
  except Exception as e:
    print(f"Exception during startup: {e}")
    raise

def run_seed():
  logger.info("Running seed file ...")
  seed_service.create_seed()
  
app = FastAPI(lifespan=lifespan, title='Forecasting')

app.mount("/src/admin", StaticFiles(directory="./src/admin"), name="admin")

origins = ['http://localhost:3000', 'http://localhost:8000', 'https://localhost:3000', 'https://localhost:8000']
# Set all CORS enabled origins
if config.BACKEND_CORS_ORIGINS:
  origins_raw = config.BACKEND_CORS_ORIGINS.split(",")
  for origin in origins_raw:
    use_origin = origin.strip()
    origins.append(use_origin)
  app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
  ),

app.include_router(api_router)
