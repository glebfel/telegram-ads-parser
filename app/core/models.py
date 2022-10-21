from datetime import date
from pydantic import BaseModel, constr, conint, confloat, Field

Euro = confloat(ge=0)


class StatsElem(BaseModel):
    date: date
    views: conint(ge=0) = Field(..., description='Number of views')
    joined: conint(ge=0) = Field(..., description='Number of new channel/chat members')
    spent: Euro = Field(..., description='Amount of money (in Euros) spent on promotion in this day')


class Statistics(BaseModel):
    tg_link: constr(max_length=255) = Field(..., description='Telegram channel url')
    status: constr(max_length=255) = Field(..., description='Status of the promotion')
    cpm: Euro = Field(..., description='CPM value')
    total_views: conint(ge=0) = Field(..., description='Total views count for the whole period')
    total_joined: conint(ge=0) = Field(..., description='Total number of new users joined for the whole period')
    total_spent: Euro = Field(...,
                              description='Total amount of money (in Euros) spent on promotion for the whole period')
    subscriber_cost: Euro = Field(..., description='Average subscriber cost')
    graph_stats: list[StatsElem] = Field(..., description='Statistics for each day of the whole period')
