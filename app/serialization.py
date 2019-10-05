from bs4 import BeautifulSoup


class Serializer:
    @staticmethod
    def serialize_urls(html: str) -> list:
        soup = BeautifulSoup(html, 'html.parser')
        page_box = soup.find('table', class_='pag_table')
        page_urls = page_box.find_all('a')

        urls = []
        for url in page_urls:
            if 'Сторінка' in url['title']:
                urls.append(url['href'])

        return urls

    @staticmethod
    def serialize_news(html: str) -> list:
        soup = BeautifulSoup(html, 'html.parser')
        news_box = soup.find('div', class_='curpane')
        page_news = news_box.find_all('article')

        news = []
        for obj in page_news:
            data = dict()

            data['title'] = obj.find('h3').text
            date = obj.find('time').text.split(' ')
            data['date'] = date[0]
            data['time'] = date[1]
            data['text'] = obj.find('div', class_='anounce').find('a').text
            data['url'] = obj.find('h3').find('a')['href']
            try:
                data['img-url'] = obj.find('img')['src']
            except TypeError:
                data['img-url'] = ''

            news.append(data)
        return news
