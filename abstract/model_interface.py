from abc import abstractmethod, ABC


class AbstractModelInterface(ABC):
    @abstractmethod
    def predict(self, news_item_content: str) -> float:
        pass
