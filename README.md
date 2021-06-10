# Python Webpage Crawlers

Various crawlers built with Selenium/Python 3/chromedriver and using Beautiful Soup to find information

## Prerequisites

* Python 3 & pip
* chromedriver - https://chromedriver.chromium.org/downloads
* beautifulsoup4 (Beautiful Soup 4)
* selenium
* xslxwriter

## find-details_linear_chromedriver.py
>>> python find-details_linear_chromedriver.py
Using a list of URLs, find needles (strings) among various page properties like canonical tags, alternatelang, anchors, pdfs, status codes, form attributes, iframe src tags

## find-urls-with-pattern_recursive_response.py
>>> python find-urls-with-pattern_recursive_response.py
Provide a starting URL and a URL pattern to match and it will crawl all links matching that pattern and list out all the anchors on the pages (unique + all)

## find-urls-with-pattern_recursive_chromedriver.py
>>> python find-urls-with-pattern_recursive_chromedriver.py
Provide a starting URL and a URL pattern to match and it will crawl all links matching that pattern and list out all the anchors on the pages (unique + all)

## single-page-audit_chromedriver.py
>>> python single-page-audit_chromedriver.py
Lists out all the anchors and anchor details

## Contributors

Warren Shea

[warrenshea.com](http://www.warrenshea.com)
[warrenshea.github.io](https://warrenshea.github.io)

