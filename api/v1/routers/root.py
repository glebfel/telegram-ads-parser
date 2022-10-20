from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def root():
    return 'This is root path of the v1 API. You can get the documentation on /docs path.'
