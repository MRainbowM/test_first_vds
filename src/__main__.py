import uvicorn
from fastapi import FastAPI

from .config import settings
from .routes import router

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(router)

if __name__ == '__main__':
    uvicorn.run(
        # app,
        "src.__main__:app",
        host=settings.HOST,
        port=settings.PORT,
        log_level=settings.LOG_LEVEL,
        debug=True
    )
