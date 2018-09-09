from distutils.core import setup


setup(
    name='scraper',
    version='1.0',
    url='https://github.com/james-o-johnstone/article-scraper',
    description='Tool to scrape articles at a given URL',
    entry_points={
        'console_scripts': [
            'scrape=scraper.scraper:run'
        ]
    },
    author='James Johnstone',
    author_email='johnstone.james@outlook.com',
    packages=['scraper'],
)