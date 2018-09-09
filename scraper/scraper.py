import argparse
import json
import logging
import os
import pprint
import requests

from scraper.parsers import get_parser, ParserFailed, UnsupportedParser


logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s:%(asctime)s: %(message)s',
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


argparser = argparse.ArgumentParser(
    description="Extract title and body from HTML and pdf articles",
)
argparser.add_argument(
    'urls',
    type=str,
    nargs='+',
    help="the url/urls of HTML articles",
)
argparser.add_argument(
    '-O',
    type=str,
    nargs='?',
    dest='output_dir',
    default='articles',
    help="output directory",
)
argparser.add_argument(
    '--dry-run',
    dest='dryrun',
    action='store_true',
    help="scraped data is printed to stdout, no articles are saved",
)


def scrape(urls):
    articles = []
    for url in urls:
        logger.info('Attempting to scrape: %s', url)

        try:
            head = requests.get(url, stream=True)
        except Exception as e:
            logger.exception('Unable to scrape %s: %s', url, e)
            continue
        else:
            # Only need headers at this stage to get the correct parser for
            # the content type. Not all servers accept HEAD requests reliably.
            head.connection.close()

        if not head.ok:
            logger.critical(
                'Unable to scrape %s, received http status code: %s',
                url,
                head.status_code,
            )
            continue

        if head.history:
            logger.info('Request to %s was redirected to %s', url, head.url)

        try:
            Parser = get_parser(head.headers['Content-Type'])
        except UnsupportedParser as e:
            logger.critical('Unable to scrape %s: %s', url, str(e))
            continue

        parser = Parser()
        try:
            article = parser.parse(head.url)
        except ParserFailed:
            logger.critical('Parser failure, unable to scrape %s', url)
            continue

        articles.append(article)

        logger.info("Successfully scraped from %s", head.url)
        logger.debug(pprint.pformat(article.jsonify()))

    return articles

def save_articles(articles, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for article in articles:
        filename = article.title + '.json'
        with open(os.path.join(output_dir, filename), 'w') as f:
            logger.info("Saving article to: %s", f.name)
            json.dump(article.jsonify(), f, indent=4, sort_keys=True)

def run():
    args = argparser.parse_args()

    articles = scrape(args.urls)

    if not args.dryrun:
        save_articles(articles, args.output_dir)
    else:
        for article in articles:
            logger.info(pprint.pformat(article.jsonify()))