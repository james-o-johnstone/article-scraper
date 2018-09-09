import unittest

from scraper.parsers import get_parser, HTMLParser


class TestParser(unittest.TestCase):

    def test_get_html_parser(self):
        content_type = 'text/html; charset=utf-8'
        Parser = get_parser(content_type)
        self.assertEqual(Parser, HTMLParser)
