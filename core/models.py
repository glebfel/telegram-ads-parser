from datetime import date
from pydantic import BaseModel, constr, conint, confloat

Euro = confloat(ge=0)


class StatsElem(BaseModel):
    date: date
    views: conint(ge=0)
    joined: conint(ge=0)


class Statistics(BaseModel):
    tg_link: constr(max_length=255)
    status: constr(max_length=255)
    cpm: Euro
    total_views: conint(ge=0)
    total_joined: conint(ge=0)
    total_spent: Euro
    subscriber_cost: Euro
    graph_stats: list[StatsElem]
