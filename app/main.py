import uvicorn
from api import statistics, root
from fastapi import FastAPI
from core import settings

app = FastAPI()
v1 = FastAPI()
v1.include_router(statistics.router)
v1.include_router(root.router)
app.mount('/v1', v1)

if __name__ == "__main__":
    uvicorn.run(app, host=settings.FAST_API_HOST, port=settings.FAST_API_PORT)