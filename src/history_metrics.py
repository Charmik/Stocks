from typing import Any, Union

from cache import Cache


class HistoryMetrics:

    def __init__(self, stock: str):
        cache_res = Cache.load_obj("obj/companies/" + stock + ".pkl")
        if cache_res is None:
            cache_res = ()
        self.data: Union[int, Any] = cache_res

    def get_income_list(self):
        income = []
        for current in self.data:
            income.append(current['netIncomePerShare'])
        return income

    def get_operation_cash_flow_per_share(self):
        operating_cash_flow_per_share = []
        for current in self.data:
            operating_cash_flow_per_share.append(current['operatingCashFlowPerShare'])
        return operating_cash_flow_per_share
