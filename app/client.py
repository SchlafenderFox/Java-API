import requests_async as request
from requests.exceptions import ConnectionError

__all__ = ['Client']


class Client:
    @staticmethod
    async def get_html(url: str) -> str:
        while True:
            async with request.Session() as session:
                try:
                    response = await session.get(url=url)
                    break
                except ConnectionError:
                    pass
        return response.text
