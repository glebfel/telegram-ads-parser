import asyncio

from parser.parse_statistic import collect_data

print(asyncio.run(collect_data('https://promote.telegram.org/stats/c4SW0pEXJ9fiA5of')))