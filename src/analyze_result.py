class AnalyzeResult:

    def __init__(self, ticker: str, pe: float, percent_pe_less_than_history: float,
                 current_ev_over_ebitda: float, percent_ev_to_ebitda_less_than_history: float):
        self.ticker = ticker
        self.pe = pe
        self.percent_pe_less_than_history = percent_pe_less_than_history
        self.current_ev_over_ebitda = current_ev_over_ebitda
        self.percent_ev_to_ebitda_less_than_history = percent_ev_to_ebitda_less_than_history
