from fastapi import APIRouter, Depends
from fastapi.security.api_key import APIKey

from api.v1.auth import get_api_key

router = APIRouter()


@router.get("/")
async def root(api_key: APIKey = Depends(get_api_key)):
    return 'This is root path of the v1 API. You can get the documentation on /docs path.'
