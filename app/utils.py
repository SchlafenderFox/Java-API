from datetime import datetime, timedelta

from bs4 import BeautifulSoup

__all__ = ['Singleton', 'Helper', 'DateManage', 'Tester']


class Singleton(type):
    _instances = dict()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Helper(metaclass=Singleton):
    @staticmethod
    def __form_base(language: str) -> str:
        choose = \
            {
                'ua': 'https://censor.net.ua/ua/news/all/page/1/archive/{date}/category/{category_id}/sortby/date',
                'ru': 'https://censor.net.ua/news/all/page/1/archive/{date}/category/{category_id}/sortby/date',
                'en': 'https://censor.net.ua/en/news/all/page/1/archive/{date}/category/{category_id}/sortby/date'
            }
        url = choose[language]
        return url

    @staticmethod
    def __rewrite_date(date: str) -> str:
        date = DateManage.convert_from_str(date=date)
        date = DateManage.convert_to_str(date=date, form='%Y-%m-%d')
        return date

    @staticmethod
    def __get_category_id(category: str) -> str:
        category_list = \
            {
                "Всі": '0',
                "Економіка": '102',
                "За кордоном": '110',
                "Здоров'я": '111',
                "Київські новини": '105',
                "Курйози": '103',
                "Події": '104',
                "Політика України": '101',
                "Спорт": '108',
                "Суспільство": '107',
                "Технології": '112',
                "Фоторепортаж": '109',
                "Шоу-бізнес": '391'
            }
        return category_list[category]

    @staticmethod
    def rewrite_json(js: dict) -> dict:
        check_dict = \
            {
                'category': 'Всі',
                'time': '00:00-23:59',
                'date': DateManage.convert_to_str(DateManage.date_now()),
                'language': 'ua'
            }

        for key in check_dict.keys():
            if key not in js or js.get(key) == '':
                js[key] = check_dict[key]
        return js

    def form_url(self, date: str, category: str, language: str) -> str:
        url = self.__form_base(language=language)
        date = self.__rewrite_date(date=date)
        category_id = self.__get_category_id(category=category)

        url = url.format(date=date, category_id=category_id)

        return url

    @staticmethod
    def filtered_time_news(news_list: list, start_time: datetime, end_time: datetime) -> list:
        filtered_news = []
        for news in news_list:
            current_time = DateManage.convert_from_str(news['time'], form="%H:%M")
            if Tester.test_time_interval(start_time=start_time,
                                         time=current_time,
                                         end_time=end_time):
                filtered_news.append(news)
        return filtered_news


class DateManage(metaclass=Singleton):
    @staticmethod
    def convert_from_str(date: str, form: str = '%d.%m.%Y') -> datetime:
        date = datetime.strptime(date, form)
        return date

    @staticmethod
    def convert_to_str(date: datetime, form: str = '%d.%m.%Y') -> str:
        return date.strftime(form)

    @staticmethod
    def date_now() -> datetime:
        return datetime.now()

    @staticmethod
    def generate_day_list(start_date: datetime, end_date: datetime) -> list:
        day_list = []
        date = start_date

        day_list.append(DateManage.convert_to_str(date=date))
        while date < end_date:
            date = date + timedelta(days=1)
            day_list.append(DateManage.convert_to_str(date=date))
        return day_list


class Tester(metaclass=Singleton):
    @staticmethod
    def test_time_interval(start_time: datetime, time: datetime, end_time: datetime) -> bool:
        if start_time <= time <= end_time:
            return True
        else:
            return False

    @staticmethod
    def test_date(date: str, form: str = '%d.%m.%Y') -> bool:
        dates = date.split('-', maxsplit=1)
        for date in dates:
            try:
                datetime.strptime(date, form)
            except ValueError:
                return False
        return True

    @staticmethod
    def test_time(time: str, form: str = '%H:%M') -> bool:
        times = time.split('-', maxsplit=1)
        for time in times:
            try:
                datetime.strptime(time, form)
            except ValueError:
                return False
        return True

    @staticmethod
    def test_language(language: str) -> bool:
        allow_language = \
            [
                'ua',
                'ru',
                'en'
            ]
        if language in allow_language:
            return True
        else:
            return False

    @staticmethod
    def test_category(category: str) -> bool:
        allow_category = \
            [
                "Всі",
                "Економіка",
                "За кордоном",
                "Здоров'я",
                "Київські новини",
                "Курйози",
                "Події",
                "Політика України",
                "Спорт",
                "Суспільство",
                "Технології",
                "Фоторепортаж",
                "Шоу-бізнес"
            ]

        if category in allow_category:
            return True
        else:
            return False

    @staticmethod
    def test_pages_in_page(html: str) -> bool:
        soup = BeautifulSoup(html, 'html.parser')
        if soup.find('table', class_='pag_table'):
            return True
        else:
            return False

    @staticmethod
    def test_news_in_page(html: str) -> bool:
        soup = BeautifulSoup(html, 'html.parser')
        if soup.find('div', class_='empty'):
            return False
        else:
            return True
