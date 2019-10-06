import logging
import asyncio

from app.client import Client
from app.utils import Tester, Helper
from app.serialization import Serializer

__all__ = ['Parser']


class Parser:
    @staticmethod
    async def __get_all_urls(url: str) -> list:
        html = await Client.get_html(url=url)
        if Tester.test_pages_in_page(html):
            urls = Serializer.serialize_urls(html)
            return urls
        else:
            return [url]

    @staticmethod
    async def __get_news_from_page(url: str) -> list:
        html = await Client.get_html(url=url)

        logging.info("Getting news from:" + url)
        if Tester.test_news_in_page(html):
            page_news = Serializer.serialize_news(html)
            return page_news
        else:
            return []

    async def __parse(self, url: str):
        urls = await self.__get_all_urls(url=url)
        page_news = []

        for url in urls:
            sub_page = await self.__get_news_from_page(url=url)
            for news in sub_page:
                page_news.append(news)

        return page_news

    async def start(self, parsed_data: dict) -> list:
        news = []

        for url in parsed_data['urls']:
            pages = await self.__parse(url=url)
            for page_news in pages:
                news.append(page_news)

        filtered_news = Helper.filtered_time_news(news_list=news, start_time=parsed_data['start-time'],
                                                  end_time=parsed_data['end-time'])

        return filtered_news
