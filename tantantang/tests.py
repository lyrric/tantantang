import asyncio

from django.test import TestCase

# Create your tests here.
from tantantang import ttt_http
from tantantang.logging_config import get_logger

log = get_logger(__name__)


def test_get_city_list():
    result = asyncio.run(ttt_http.get_city_list())
    result_dict = [city.to_dict() for city in result]
    log.info(result_dict)


def test_get_activity_list():
    result = asyncio.run(ttt_http.get_activity_list(1, 10, '成都市'))
    result_dict = [activity.__str__() for activity in result]
    log.info(result_dict)


def test_bar_gain():
    result = asyncio.run(ttt_http.bar_gain('', '', '', None))
    log.info(result)


def test_get_activity_detail():
    result = asyncio.run(
        ttt_http.get_activity_detail('', 32790, 1,
                                     1))
    log.info(result)


test_get_activity_detail()
