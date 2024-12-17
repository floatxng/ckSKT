import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, List
from abc import ABC, abstractmethod
from abstract.news_parser import AbstractNewsParser, NewsItem
from abstract.stock_market_parser import AbstractStockMarketParser
from implementations.telegram_news_parser import TelegramNewsParser
from implementations.moex_stock_market_parser import MoexStockMarketParser


class DataGenerator:
    def __init__(self, news_parser: AbstractNewsParser, stock_parser: AbstractStockMarketParser):
        self.news_parser = news_parser
        self.stock_parser = stock_parser

    def calculate_market_reaction(self, stock: str, news_time: datetime) -> float:
        start_time = news_time
        end_time_5min = news_time + timedelta(minutes=5)
        end_time_55min = news_time + timedelta(minutes=55)

        prices = self.stock_parser.parse_prices_1min(stock, start_time, end_time_55min)
        if len(prices) < 6:
            return 0.0

        price_0 = prices[0]
        price_5min = prices[5]
        price_55min = prices[-1]

        change_5min = (price_5min - price_0) / price_0
        change_55min = (price_55min - price_0) / price_0

        reaction = 0.7 * change_5min + 0.3 * change_55min
        return reaction

    def generate_data(self, count: int, output_file: str, start_date=None, end_date=None):
        news_items = self.news_parser.parse_all_news(count_limit=count, start_date=start_date, end_date=end_date)
        # TODO: сделать parse_all_news генератором
        data = []

        for news in news_items:
            print(news['date'], news['stock'])
            reaction = self.calculate_market_reaction(news['stock'], news['date'])
            if abs(reaction) > 0.001:
                data.append({
                    "text": news['content'],
                    "reaction": reaction
                })

        df = pd.DataFrame(data)
        df.to_csv(output_file, index=False, encoding="utf-8")
        print(f"Данные успешно сохранены в файл: {output_file}")


if __name__ == "__main__":
    news_parser = TelegramNewsParser(["stocksi_ru"])
    stock_parser = MoexStockMarketParser()

    generator = DataGenerator(news_parser, stock_parser)
    generator.generate_data(count=1000, output_file="saved/data.csv")
