from fastapi import APIRouter, HTTPException, status

from parser import collect_data
from core import Statistics, CampaignNotExistsError

router = APIRouter()


@router.get("/get-stats/{campaign_id}", response_model=Statistics)
async def read_item(campaign_id):
    try:
        data = await collect_data(campaign_id)
    except CampaignNotExistsError as ex:
        raise HTTPException(status_code=404, detail=str(ex))
    return data
