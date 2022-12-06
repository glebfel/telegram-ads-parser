import datetime

import aiohttp as aiohttp
from bs4 import BeautifulSoup

from cache import get_from_cache, check_cache, cache_request
from core import StatsElem, Statistics, CampaignNotExistsError
from core import NotEnoughDayDataError

BASE_URL = 'https://promote.telegram.org/'

BASE_HEADER = {'Accept': '*/*',
               'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Macintosh; Intel Mac OS X 10_7_3; Trident/6.0)'}


async def parse_header_stats(promotion_id: str) -> dict | None:
    """Get stats from page header (link, status, CPM, views)"""
    # get page html-markup
    async with aiohttp.ClientSession() as session:
        async with session.get(BASE_URL + 'stats/' + promotion_id) as resp:
            page = await resp.text()

    if 'In addition to sending private messages and chatting in ' \
       'private groups, Telegram users can subscribe to' in page:
        raise CampaignNotExistsError(promotion_id)

    page_markup = BeautifulSoup(page, 'lxml')

    # find stats
    stats = page_markup.find_all(class_='pr-review-ad-info')

    # tg link
    tg_link = stats[1].contents[3].a.attrs['href']
    # status
    status = stats[2].contents[3].text.strip()
    # CPM
    cpm = float(stats[3].contents[3].text.replace('€', ''))
    # views
    total_views = stats[4].contents[3].text.replace(',', '')

    return {
        'tg_link': tg_link,
        'status': status,
        'cpm': cpm,
        'total_views': total_views
    }


async def parse_graph_stats(promotion_id: str) -> list[StatsElem] | None:
    # get graph stats in csv
    querystring = {"prefix": f"shared/{promotion_id}", "period": "day"}
    url = BASE_URL + 'csv/'
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=querystring) as resp:
            stats_csv = await resp.text()

    # convert csv in python list
    stats_list = [i.split('\t') for i in stats_csv.split('\n')][1:]
    # convert all list's elements to named dicts
    if stats_list:
        if len(stats_list[0]) > 2:
            stats_list = [StatsElem(date=datetime.datetime.strptime(i[0], '%d %b %Y'), views=i[1], joined=i[2], spent=0)
                          for i in stats_list]
        else:
            raise NotEnoughDayDataError(promotion_id)

    return stats_list


async def collect_data(promotion_id: str) -> Statistics:
    # check if data already in redis
    if check_cache(promotion_id):
        return get_from_cache(promotion_id)

    # collect header stats
    header_stats = await parse_header_stats(promotion_id)

    # collect graph stats
    graph_stats = await parse_graph_stats(promotion_id)

    # calculate spent value for each day and add to the list
    for i in graph_stats:
        # cost per day = (views * cpm / 1000)/0.8
        # 0.8 - SJ commission
        i.spent = round(((i.views * header_stats['cpm'] / 1000) / 0.8), 3)

    # calculate other total values (total_joined, total_spent, subscriber_cost)
    total_joined = sum([i.joined for i in graph_stats])
    # cost per day = views * cpm / 1000
    total_spent = sum([i.spent for i in graph_stats])
    # subscriber_cost = total_spent/total_joined
    subscriber_cost = round(total_spent / total_joined, 2)

    # convert to Statistics object
    statistics = Statistics(**header_stats,
                            total_joined=total_joined,
                            total_spent=total_spent,
                            subscriber_cost=subscriber_cost,
                            graph_stats=graph_stats)

    # cache request
    cache_request(promotion_id, statistics)

    return statistics
