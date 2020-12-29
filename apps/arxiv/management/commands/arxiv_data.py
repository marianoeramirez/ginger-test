import functools
import logging
from datetime import datetime, timedelta

import feedparser
from django.core.management.base import BaseCommand
from django.utils import timezone

from ... import models

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Fetch the Articles and Authors from the Arxiv API"
    template_url = (
        "http://export.arxiv.org/api/query?"
        "search_query=all:psychiatry%20OR%20all:therapy%20OR%20all:data%20science%20OR%20all:machine%20learning"
        "&start={start}&max_results={items_page}"
        "&sortBy=submittedDate&sortOrder=descending"
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--items_page",
            default=100,
            type=int,
            help="Define how many items should fetch by page (default:100)",
        )
        parser.add_argument(
            "--limit_days",
            default=180,
            type=int,
            help="Define the max number of days to be fetched (default:180)",
        )

    @functools.lru_cache(maxsize=128)
    def get_or_create_author(self, name: str) -> models.Author:
        """
        This function get or create an author
        :param name: Name to be searched on the database
        :return: the author associated with the name
        """
        instance, is_new = models.Author.objects.get_or_create(name=name)
        return instance

    def query_page(self, start: int, items_page: int, min_date: datetime) -> bool:
        """
        Call the api of arxiv and process the information
        :param start: start parameter for the URL, that is an index
        :param items_page: number of items per page passed to the URL
        :param min_date: minimum date to be processed from the API
        :return:  return bool that indicate if there are more pages or not"""

        URL = self.template_url.format(start=start, items_page=items_page)
        logger.info("URL: " + URL)
        data = feedparser.parse(URL)

        for entry in data["entries"]:

            date = datetime.strptime(entry["published"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
            if date < min_date:
                return False

            instance, is_new = models.Article.objects.get_or_create(
                remote_id=entry["id"],
                title=entry["title"],
                summary=entry["summary"],
                published=date,
            )
            instance.authors.set(
                [
                    self.get_or_create_author(author["name"])
                    for author in entry["authors"]
                ]
            )

        total = int(data["feed"]["opensearch_totalresults"])
        return total > start + items_page

    def handle(self, *args, **options):
        """ Main function than handle the invocation of the command"""
        min_date = datetime.now().replace(tzinfo=timezone.utc) - timedelta(days=options.pop("limit_days"))
        items_page = options.pop("items_page")

        start = 0
        while self.query_page(start, items_page, min_date):
            logger.info("Page start: " + str(start))
            start += items_page

        logger.info("Successfully imported the information")
