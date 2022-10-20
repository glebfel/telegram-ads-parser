import datetime

import aiohttp as aiohttp
import validators
from bs4 import BeautifulSoup

from core import custom_logger, exceptions
from core.models import StatsElem, Statistics

BASE_URL = 'https://promote.telegram.org/'

BASE_HEADER = {'Accept': '*/*',
               'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Macintosh; Intel Mac OS X 10_7_3; Trident/6.0)'}


def validate_link(url: str):
    """Basic link validation"""
    # basic url validation
    if validators.url(url):
        # validate if url contains is mobel.de
        if BASE_URL in url:
            return
    raise exceptions.InvalidUrlError(url)


async def parse_header_stats(url: str) -> dict | None:
    """Get stats from page header (link, status, CPM, views)"""
    # get page html-markup
    session = aiohttp.ClientSession(headers=BASE_HEADER)
    async with session.get(url) as resp:
        page = await resp.text()
    await session.close()
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


async def parse_graph_stats(url: str) -> list[StatsElem] | None:
    # get graph stats in csv
    querystring = {"prefix": f"shared/{url.split('/')[-1]}", "period": "day"}
    url = BASE_URL + 'csv'
    session = aiohttp.ClientSession(headers=BASE_HEADER)
    async with session.get(url, params=querystring) as resp:
        stats_csv = await resp.text()
    await session.close()

    # convert csv in python list
    stats_list = [i.split('\t') for i in stats_csv.split('\n')][1:]
    # convert all list's elements to named dicts
    stats_list = [StatsElem(date=datetime.datetime.strptime(i[0], '%d %b %Y'), views=i[1], joined=i[2]) for i in
                  stats_list]

    return stats_list


async def collect_data(url: str) -> Statistics:
    # validate link
    validate_link(url)

    # collect header stats
    header_stats = await parse_header_stats(url)

    # collect graph stats
    graph_stats = await parse_graph_stats(url)

    # calculate other total values (total_joined, total_spent, subscriber_cost)
    total_joined = sum([i.joined for i in graph_stats])
    # cost per day = views * cpm / 1000
    total_spent = round(sum([i.views * header_stats['cpm'] / 1000 for i in graph_stats]), 2)
    # subscriber_cost = total_spent/total_joined
    subscriber_cost = round(total_spent/total_joined, 2)

    return Statistics(**header_stats,
                      total_joined=total_joined,
                      total_spent=total_spent,
                      subscriber_cost=subscriber_cost,
                      graph_stats=graph_stats)
