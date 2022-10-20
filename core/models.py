from datetime import date
from pydantic import BaseModel, constr, conint, confloat

Euro = confloat(ge=0)


class StatsElem(BaseModel):
    date: date
    views: conint(ge=0)
    joins: conint(ge=0)


class Statistics(BaseModel):
    tg_link: constr(max_length=255)
    status: constr(max_length=255)
    cpm: Euro
    views: conint(ge=0)
    graph_stats: list[StatsElem]
