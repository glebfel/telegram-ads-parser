from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security.api_key import APIKey

from parser import collect_data
from core import Statistics, CampaignNotExistsError
from api.v1.auth import get_api_key

router = APIRouter(tags=["statistics"])


@router.get("/get-stats/{campaign_id}", response_model=Statistics)
async def get_campaign_stats(campaign_id: str, api_key: APIKey = Depends(get_api_key)) -> Statistics:
    """Get ads campaign statistics by id"""
    try:
        data = await collect_data(campaign_id)
    except CampaignNotExistsError as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ex))
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='something goes wrong with parser ...')
    return data