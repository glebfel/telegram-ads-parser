from fastapi import APIRouter, HTTPException, status, Depends

from parser import collect_data
from core import Statistics, CampaignNotExistsError, NotEnoughDayDataError
from api.v1.auth import get_api_key

router = APIRouter(tags=["statistics"], prefix='/stats', dependencies=[Depends(get_api_key)])


@router.get("/get-stats/{promotion_id}", response_model=Statistics)
async def get_campaign_stats(promotion_id: str) -> Statistics:
    """Get ads promotion statistics by ID"""
    try:
        data = await collect_data(promotion_id)
    except CampaignNotExistsError as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ex))
    except NotEnoughDayDataError as ex:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(ex))
    except Exception:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail='something goes wrong with parser ...')
    return data
