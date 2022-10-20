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
    cpm = stats[3].contents[3].text.replace('€', '')
    # views
    views = stats[4].contents[3].text.replace(',', '')

    return {
        'tg_link': tg_link,
        'status': status,
        'cpm': cpm,
        'views': views
    }


async def parse_graph_stats(url: str) -> list[StatsElem] | None:
    # get graph stats in csv
    url = BASE_URL + 'csv'
    querystring = {"prefix": "shared/c4SW0pEXJ9fiA5of", "period": "day"}
    session = aiohttp.ClientSession(headers=BASE_HEADER)
    async with session.get(url, params=querystring) as resp:
        stats_csv = await resp.text()
    await session.close()

    # convert csv in python list
    stats_list = [i.split('\t') for i in stats_csv.split('\n')][1:]
    # convert all list's elements to named dicts
    stats_list = [StatsElem(date=datetime.datetime.strptime(i[0], '%d %b %Y'), views=i[1], joins=i[2]) for i in
                  stats_list]

    return stats_list


async def collect_data(url: str) -> Statistics:
    # validate link
    validate_link(url)

    # collect header stats
    header_stats = await parse_header_stats(url)

    # collect graph stats
    graph_stats = await parse_graph_stats(url)

    return Statistics(**header_stats, graph_stats=graph_stats)


