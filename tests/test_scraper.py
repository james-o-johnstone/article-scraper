import unittest
import os

import responses

from scraper.scraper import scrape


TESTS_DIR = os.path.dirname(os.path.realpath(__file__))
TEST_DATA_PATH = os.path.join(TESTS_DIR, 'test_data')


class TestScraper(unittest.TestCase):
    @responses.activate
    def test_html_scrape(self):
        url = "http://www.crainscleveland.com/node/688181"
        with open(os.path.join(TEST_DATA_PATH, 'article.html')) as f:
            body = f.read()
        responses.add(
            responses.GET,
            url,
            body=body,
            status=200,
            content_type='text/html; charset=utf-8',
        )

        expected_title = "Cleveland Clinic sets opening for new Lakewood Family Health Center"
        with open(os.path.join(TEST_DATA_PATH, 'html_article_body.txt')) as f:
            expected_body = f.read()

        articles = scrape([url])

        self.assertEqual(articles[0].title, expected_title)
        self.assertEqual(articles[0].body, expected_body)

    @responses.activate
    def test_bad_url(self):
        url = "http://www.bad_url.com"
        responses.add(
            responses.GET,
            url,
            body=Exception(),
        )

        articles = scrape([url])
        expected_articles = []

        self.assertEqual(articles, expected_articles)

    @responses.activate
    def test_unsupported_content_type(self):
        url = "https://www.url.com"
        responses.add(
            responses.GET,
            url,
            headers={'Content-Type': 'application/json'},
        )

        articles = scrape([url])
        expected_articles = []

        self.assertEqual(articles, expected_articles)

    @responses.activate
    def test_bad_status_code(self):
        url = "http://www.bad_url.com"
        responses.add(
            responses.GET,
            url,
            status=404,
        )

        articles = scrape([url])
        expected_articles = []

        self.assertEqual(articles, expected_articles)