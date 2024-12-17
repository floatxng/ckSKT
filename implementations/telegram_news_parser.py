import json
from datetime import datetime
import re
import snscrape.modules.telegram as telegram_scraper
import dateutil
from abstract.news_parser import AbstractNewsParser, NewsItem


class TelegramNewsParser(AbstractNewsParser):
    def __init__(self, channels, output_file="posts.json"):
        self.channels = channels
        self.output_file = output_file

    def parse_all_news(self, start_date=None, end_date=None, count_limit=0):
        all_news = []
        i = 0
        for channel in self.channels:  # TODO: сделать равномерное взятие новостей из каналов
            scraper = telegram_scraper.TelegramChannelScraper(channel)
            for post in scraper.get_items():
                if count_limit and i >= count_limit:
                    break
                if start_date and post.date < start_date:
                    continue
                if end_date and post.date > end_date:
                    continue
                if not post.content:
                    continue

                post.content = post.content.replace("@stocksi", "")
                stock_name = self._extract_stock_name(post.content)
                if stock_name:
                    news_item = NewsItem(
                        stock=stock_name,
                        content=post.content,
                        date=post.date,
                        source=channel
                    )
                    all_news.append(news_item)
                    i += 1

        return all_news

    def _extract_stock_name(self, content):
        match = re.search(r'\$(\w+)', content)
        return match.group(1) if match else None
