from fastapi import APIRouter

from parser import collect_data
from core import Statistics

router = APIRouter()


@router.get("/get-stats/{campaign_id}", response_model=Statistics)
async def read_item(campaign_id):
    data = collect_data(campaign_id)
    return data
