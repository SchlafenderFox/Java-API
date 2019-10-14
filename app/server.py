import json
import logging

import tornado.ioloop
from tornado.web import RequestHandler, Application, url

from app.parser import Parser
from app.utils import Helper, DateManage, Tester


class API(RequestHandler):
    def get(self):
        with open('./html/info.html') as f:
            self.write(f.read())


class GetNews(RequestHandler):
    async def get(self):
        params = {k: self.get_argument(k) for k in self.request.arguments}
        logging.info("Input parameters:" + str(params))
        params = Helper.rewrite_json(params)

        response_dict = \
            {
                'status': 'ok',
                'result': [],
                'error': ''
            }

        logging.info("Rewrite parameters:" + str(params))
        if not Tester.test_category(params['category']):
            response_dict['status'] = 'error'
            response_dict['error'] = 'Wrong category'
            logging.info("Json:" + str(response_dict))
            self.write(json.dumps(response_dict, ensure_ascii=False))
            await self.finish()

        elif not Tester.test_language(params['language']):
            response_dict['status'] = 'error'
            response_dict['error'] = 'Wrong language.'
            logging.info("Json:" + str(response_dict))
            self.write(json.dumps(response_dict, ensure_ascii=False))
            await self.finish()

        elif not Tester.test_time(time=params['time']):
            response_dict['status'] = 'error'
            response_dict['error'] = 'Wrong time.'
            logging.info("Json:" + str(response_dict))
            self.write(json.dumps(response_dict, ensure_ascii=False))
            await self.finish()

        elif not Tester.test_date(date=params['date']):
            response_dict['status'] = 'error'
            response_dict['error'] = 'Wrong date.'
            logging.info("Json:" + str(response_dict))
            self.write(json.dumps(response_dict, ensure_ascii=False))
            await self.finish()

        else:
            logging.info("Input parameters:" + str(params))
            days = DateManage.generate_day_list(DateManage.convert_from_str(params['date'].split('-')[0]),
                                                DateManage.convert_from_str(params['date'].split('-')[-1]))
            logging.debug('Days list:' + str(days))

            helper = Helper()
            data = \
                {
                    'start-time': DateManage.convert_from_str(params['time'].split('-')[0], form='%H:%M'),
                    'end-time': DateManage.convert_from_str(params['time'].split('-')[-1], form='%H:%M'),
                    'urls': [helper.form_url(date=day, category=params['category'], language=params['language']) for day
                             in days]
                }
            logging.debug("Parser data:" + str(data))

            parser = Parser()
            response_dict['result'] = await parser.start(parsed_data=data)
            response_dict['count'] = len(response_dict['result'])
            logging.info("Json:" + str(response_dict))

            self.write(json.dumps(response_dict, ensure_ascii=False))
            await self.finish()


def make_app():
    app = Application([
        url(r"/api/", API, name='api'),
        url(r"/api/get-news/", GetNews, name='news'),
    ])
    return app


def run():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    app = make_app()
    app.listen(9999)
    tornado.ioloop.IOLoop.current().start()
