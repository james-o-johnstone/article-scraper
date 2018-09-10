from abc import ABC, abstractmethod
import logging
import os
import re

import fitz
from goose3 import Goose
import requests
from requests.exceptions import RequestException

from scraper.models import Article


logger = logging.getLogger(__name__)


def get_parser(raw_content_type):
    content_type_match = CONTENT_TYPE_REGEX.match(raw_content_type)
    if content_type_match is None:
        raise UnsupportedParser(
            "No parser for content type: %s" % raw_content_type
        )

    return PARSERS[content_type_match.group(1)]


class BaseParser(ABC):
    @abstractmethod
    def parse(self, url):
        pass


class HTMLParser(BaseParser):
    def __init__(self):
        self.goose = Goose()

    def parse(self, url):
        try:
            article = self.goose.extract(url=url)
        except RequestException as e:
            logger.exception(e)
            raise ParserFailed

        return Article(url, article.title, article.cleaned_text)


class PDFParser(BaseParser):
    def parse(self, url):
        temp_pdf_file = self.save_pdf(url)
        title, body = self.get_title_and_body(temp_pdf_file)
        os.remove(temp_pdf_file)

        return Article(url, title, body)

    def save_pdf(self, url):
        try:
            source = requests.get(url, stream=True)
        except RequestException as e:
            logger.exception(e)
            raise ParserFailed

        filename = 'tmp_pdf.pdf'
        with open(filename, 'wb') as f:
            for chunk in source.iter_content(chunk_size=2000):
                f.write(chunk)

        return filename

    def get_title_and_body(self, pdf_file):
        doc = fitz.open(pdf_file)

        body_text = ''
        n_pages = doc.pageCount
        for page_num in range(n_pages):
            page = doc.loadPage(page_num)
            body_text += page.getText('text')

        return doc.metadata['title'], body_text


class UnsupportedParser(Exception):
    pass


class ParserFailed(Exception):
    pass


PARSERS = {
    'application/pdf': PDFParser,
    'text/html': HTMLParser,
}

SUPPORTED_CONTENT_TYPES = PARSERS.keys()

CONTENT_TYPE_REGEX = re.compile(
    r".*(" + r"|".join(SUPPORTED_CONTENT_TYPES) + r").*"
)