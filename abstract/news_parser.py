from abc import abstractmethod, ABC
from datetime import datetime
from typing import Optional, List
from typing import TypedDict


class NewsItem(TypedDict):
    stock: str
    content: str
    date: datetime
    source: str


class AbstractNewsParser(ABC):
    @abstractmethod
    def parse_all_news(self, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None,
                       count_limit: int = 0) -> List[NewsItem]:
        pass


