# Article Scraper

## About
A command line tool written in Python (3.7) to scrape HTML and PDF articles from a given url.

## Installation
1. Install Python 3
2. cd to the project folder.
3. Create and activate a virtual env, e.g.: `python3 -m virtualenv env && source env/bin/activate`
4. Install required libraries: `pip install -r requirements.txt`
5. Install the application `pip install .`

## Tests
1. Ensure that you are in the virtualenv where you installed the libraries (see step 3 in Installation)
2. cd to the project folder and: `python -m unittest discover -s tests`

## Documentation
To view available command line options, in a terminal type: `scrape -h`.

## Examples
#### To view the title and body that will be scraped from a URL 
`scrape $url --dry-run` where `$url` is the URL you wish to scrape (content type must be HTML/PDF).

#### To scrape a URL and save the title, body and URL in a JSON file
`scrape $url`
The JSON files will be saved in a `/articles` directory. The directory will be created if it doesn't exist.

#### To scrape a URL and save the title, body and URL in a JSON file in a custom directory
`scrape $url /path/to/custom/directory`

#### To scrape multiple URLS
`scrape $url1 $url2 $url3`
