import sys

from loguru import logger

logger.remove(0)
logger.add(sys.stderr, colorize=True)
logger.add('logs.log', level='INFO', rotation='100 MB', compression='zip', mode='w')
custom_logger = logger.bind(specific=True)