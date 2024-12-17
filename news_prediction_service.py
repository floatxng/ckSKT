from abstract.stock_market_parser import AbstractStockMarketParser
from abstract.model_interface import AbstractModelInterface
from abstract.news_parser import AbstractNewsParser


class NewsPredictionService:
    def __init__(self,
                 stock_market_parser: AbstractStockMarketParser,
                 model_interface: AbstractModelInterface,
                 news_parser: AbstractNewsParser):
        self._stock_market_parser = stock_market_parser
        self._model_interface = model_interface
        self._news_parser = news_parser

    def get_last_news_with_precise_predictions(self, news_count: int):
        news = self._news_parser.parse_all_news(count_limit=news_count)
        results = []
        for new_item in news:
            price_change_prediction = self._model_interface.predict(new_item["content"])
            current_price = self._stock_market_parser.get_current_price(new_item["stock"])
            predicted_price = current_price * (1 + price_change_prediction)
            results.append([*new_item.values(), current_price, predicted_price])

        return results
