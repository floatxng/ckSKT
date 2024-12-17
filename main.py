from implementations.logistic_regression_model import LogisticRegressionAbstractModelInterface
from implementations.telegram_news_parser import TelegramNewsParser
from implementations.moex_stock_market_parser import MoexStockMarketParser
from news_prediction_service import NewsPredictionService

news_parser = TelegramNewsParser(channels=["stocksi_ru"])
stock_parser = MoexStockMarketParser()
model = LogisticRegressionAbstractModelInterface()

service = NewsPredictionService(stock_parser, model, news_parser)

results = service.get_last_news_with_precise_predictions(news_count=5)
print([(result[0], result[1], result[-1], result[-2]) for result in results])

