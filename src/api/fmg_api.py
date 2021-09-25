import os
import string

import requests
from cache import Cache


class FmgAPI:

    API_KEY: string = os.environ['FINANCIAL_MODELING_GREP_API']
    BASE_PATH = "obj"

    @staticmethod
    def get_key_metrics(ticker: string):
        path = FmgAPI.BASE_PATH + "/key-metrics-ttl"
        if not os.path.exists(path):
            os.mkdir(path)

        path: string = path + "/" + ticker
        cache_result = Cache.load_obj(path)
        if cache_result is None:
            data = requests.get(
                f"https://financialmodelingprep.com/api/v3/key-metrics-ttm/{ticker}?apikey={FmgAPI.API_KEY}")
            # check for None
            data = data.json()
            data = data[0]
            Cache.save_obj(data, path)
            return data
        else:
            return cache_result

    @staticmethod
    def get_quote_metrics(ticker: string):
        path = FmgAPI.BASE_PATH + "/quote_metrics"
        if not os.path.exists(path):
            os.mkdir(path)

        path: string = path + "/" + ticker
        cache_result = Cache.load_obj(path)
        if cache_result is None:
            data = requests.get(
                f"https://financialmodelingprep.com/api/v3/quote/{ticker}?apikey={FmgAPI.API_KEY}")
            # check for None
            data = data.json()
            data = data[0]
            Cache.save_obj(data, path)
            return data
        else:
            return cache_result
