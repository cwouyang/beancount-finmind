from datetime import datetime

import pytz
import requests
from beancount.core.number import D

try:
    from beanprice import source
except ImportError:
    from beancount.prices import source


class Source(source.Source):
    API_ENDPOINT = 'https://api.finmindtrade.com/api/v4/data'
    DATE_FORMAT = '%Y-%m-%d'

    @staticmethod
    def _get_price(ticker, time=None):
        dataset, data_id, quote_currency = ticker.split(':')
        if time is None:
            date = datetime.utcnow().replace(tzinfo=pytz.utc)
        else:
            date = time
        # https://finmind.github.io/quickstart/#api_1
        parameter = {
            "dataset": dataset,
            "data_id": data_id,
            "start_date": (date.strftime(Source.DATE_FORMAT)),
        }
        resp = requests.get(Source.API_ENDPOINT, params=parameter)
        data = resp.json()["data"]
        if len(data) == 0:
            # No data today
            return None

        close_price = data[0]["close"]
        price = D(close_price).quantize(D('0.00'))
        return source.SourcePrice(price, date, quote_currency)

    def get_latest_price(self, ticker):
        return self._get_price(ticker)

    def get_historical_price(self, ticker, time):
        return self._get_price(ticker, time)
