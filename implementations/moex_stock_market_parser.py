import requests
from datetime import datetime, timedelta
from abstract.stock_market_parser import AbstractStockMarketParser


class MoexStockMarketParser(AbstractStockMarketParser):
    def __init__(self):
        self.base_url = "http://iss.moex.com/iss/engines/stock/markets/shares/securities"

    def parse_prices_1min(self, stock, start_date=None, end_date=None):
        start_date = start_date or datetime.now() - timedelta(minutes=10)
        end_date = end_date or datetime.now()

        url = f"{self.base_url}/{stock}/candles.json?from={start_date}&till={end_date}&interval=1"
        response = requests.get(url)
        if response.status_code != 200:
            return []

        data = response.json()

        candles = [
            {k: r[i] for i, k in enumerate(data['candles']['columns'])}
            for r in data['candles']['data']
        ]

        if len(candles) < 2:
            return []

        prices = [row[1] for row in data['candles']['data']]  # Цена закрытия

        return tuple(prices)

    def get_current_price(self, stock):
        now = datetime.now()
        attempts = [10, 60, 24 * 60]
        current_price = 0.0

        for attempt in attempts:
            try:
                prices = self.parse_prices_1min(stock, start_date=now - timedelta(minutes=attempt), end_date=now)
                if prices:
                    current_price = prices[-1]
                if current_price > 0:
                    return current_price
            except Exception as e:
                pass

        print(f"[WARNING] Не удалось получить актуальную цену для {stock}, возвращено: {current_price}")
        return current_price
