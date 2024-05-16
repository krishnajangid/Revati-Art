import logging
import time

import uvicorn
from fastapi import FastAPI
from fastapi import Request
from fastapi_sqlalchemy import DBSessionMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from admin.admin import UserAdmin, ProductAdmin, CategoryAdmin
from api import router
from utils.config import settings
from utils.logging_config import CustomLogFilter, LOGGING_CONFIG
from utils.model_base import engine
from sqladmin import Admin

logging.config.dictConfig(LOGGING_CONFIG)

app = FastAPI(openapi_url=f"{settings.API_V1_STR}/openapi.json")
admin = Admin(app, engine)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(
    DBSessionMiddleware,
    db_url="postgresql://{user}:{password}@{host}/{database}?sslmode=require".format(
        user=settings.PG_USER,
        password=settings.PG_PASSWORD,
        database=settings.DB_NAME,
        host=settings.PG_HOST,
    )

)


@app.middleware("http")
async def log_stuff(request: Request, call_next):
    CustomLogFilter.request_id = request.headers.get('X-Req-Id') or f'req_{int(time.time() * 1000)}'

    return await call_next(request)


@app.exception_handler(Exception)
async def exception_error_handler(request: Request, exc: Exception):
    logging.error(f"Error while process data. Error: {exc}.")
    return JSONResponse(
        status_code=500,
        content={"message": "Something went wrong. Please try agan later."},
    )


admin.add_view(UserAdmin)
admin.add_view(CategoryAdmin)
admin.add_view(ProductAdmin)
app.include_router(router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    uvicorn.run("run:app", host="0.0.0.0", port=5050, reload=True)
