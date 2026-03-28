import argparse
import asyncio
import logging
import aiohttp
from dataclasses import dataclass
from html.parser import HTMLParser as _HTMLParser

from typing import List


class HTMLParser(_HTMLParser):

    def __init__(self):
        super().__init__()
        self.links = []
        self.data = []

    def __enter__(self):
        self.reset()
        self.links = []
        self.data = []
    
    def __exit__(self, *args):
        self.reset()
        self.links = []
        self.data = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.links.append(attrs[0][1])

    def handle_data(self, data):
        self.data.append(data)


@dataclass
class CrawlResults:
    path: str
    links: List[str]
    data: List[str]


class Crawler:
    def __init__(self, root):
        self.root = root
        self.visited = dict()
        self.html_parser = HTMLParser()

        logging.info(f"Initialized crawler for {root}")

    async def crawl(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.root) as request:
                with self.html_parser:
                    self.html_parser.feed(await request.text())
                    self.visited[self.root] = CrawlResults(self.root, self.html_parser.links, self.html_parser.data)

    def stats(self):
        return "\n\n".join([f"""
        Path: {result.path}
        links: {len(result.links)}
        data: {sum([len(data) for data in result.data])}
        """ for result in self.visited.values()])

def main():
    parser = argparse.ArgumentParser(description="Web Crawler POC")
    
    # Add your arguments here
    parser.add_argument("urls", nargs="+", action='extend', help="The root URL to start crawling")
    parser.add_argument("-d", "--depth", type=int, default=2, help="Crawling depth (default: 2)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Increase output verbosity")

    args = parser.parse_args()

    # Access your args
    log_level = logging.INFO
    if args.verbose:
        log_level = logging.DEBUG
    
    logging.basicConfig(level=log_level, format="%(asctime)s:%(levelname)s - %(message)s", datefmt='%Y-%m-%dT%H:%M:%S%z')
    
    crawlers = [Crawler(url) for url in args.urls]

    async def main():
        await asyncio.gather(*[crawler.crawl() for crawler in crawlers])

    asyncio.run(main())

    for crawler in crawlers:
        logging.info(crawler.stats())

    logging.info(f"Finished crawling")


if __name__ == "__main__":
    main()
