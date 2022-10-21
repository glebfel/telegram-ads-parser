import uvicorn
from api import statistics, root
from fastapi import FastAPI
from core import settings
from fastapi.middleware.cors import CORSMiddleware

# define allowed origins for CORS
origins = [
    "http://localhost:8888",
    "https://telejet.socialjet.pro"
]

# init api instances
app = FastAPI(title='Telegram Ads Statistics')
v1 = FastAPI(title='Telegram Ads Statistics')
v1.include_router(statistics.router)
v1.include_router(root.router)
app.mount('/v1', v1)

# mount middleware to instances
v1.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app, host=settings.FAST_API_HOST, port=settings.FAST_API_PORT)