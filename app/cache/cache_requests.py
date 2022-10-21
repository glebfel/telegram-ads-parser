import json
from datetime import timedelta, datetime

import redis

from core import settings, Statistics

# init redis server
cache = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


def time_until_end_of_day(dt=None):
    """Calculate number of seconds till the end of the day"""
    if dt is None:
        dt = datetime.now()
    return ((24 - dt.hour - 1) * 60 * 60) + ((60 - dt.minute - 1) * 60) + (60 - dt.second)


def cache_request(campaign_id: str, data: Statistics):
    cache.setex(name=campaign_id, value=data.json(), time=timedelta(seconds=time_until_end_of_day()))


def check_cache(campaign_id: str) -> bool:
    if cache.exists(campaign_id):
        return True
    return False


def get_from_cache(campaign_id: str) -> Statistics:
    return Statistics(**json.loads(cache.get(campaign_id)))
