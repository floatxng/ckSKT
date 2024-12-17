from abc import abstractmethod, ABC
from datetime import datetime
from typing import Optional


class AbstractStockMarketParser(ABC):
    @abstractmethod
    def parse_prices_1min(self, stock: str,
                          start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> tuple:
        pass

    @abstractmethod
    def get_current_price(self, stock: str) -> float:
        pass