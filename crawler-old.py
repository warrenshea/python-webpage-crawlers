import requests
import re
import xlsxwriter
from urlparse import urlparse
from lxml import html

class Crawler():
    base = "https://www.domain.com"
    start_link = "https://www.domain.com/home/"
    pattern_to_match = "/home"
    visited_links = []
    filtered_links = []

    def __init__(self):
        self.crawl_url(self.start_link)
        self.print_visited_links()

    def filter_link(self, url):
        url = urlparse(url).path

        # Replace any accidental // with /
        url = url.replace("//","/")

        # If it's a file
        if url.find(".") != -1:
            return

        if url.find("popup(") != -1:
            return

        if url.find("javascript(") != -1:
            return

        # Add Trailing Slash for consistency
        if not url.endswith("/"):
            url = url + "/"

        # URL must match pattern_to_match
        if url.find(self.pattern_to_match) != -1:
            return url
        else:
            return

    def crawl_url(self, url):
        print("root url: " + url)
        self.visited_links.append(url)

        response = requests.get(url)
        tree = html.fromstring(response.text)

        all_links_raw = tree.xpath("/html/body//a/@href")
        for raw_link in all_links_raw:
            link = self.filter_link(raw_link)
            #print(link)
            if (link is not None) and link not in self.visited_links:
                self.filtered_links.append(link)

        for next_url in self.filtered_links:
            full_url = str(self.base + next_url)
            if full_url not in self.visited_links:
                self.crawl_url(full_url)

    def print_visited_links(self):
        print("************");
        print("All links");
        print(self.visited_links);
        workbook = xlsxwriter.Workbook('results.xlsx')
        worksheet = workbook.add_worksheet()
        row = 0
        column = 0
        for item in self.visited_links:
            worksheet.write(row,column,item)
            row += 1
        workbook.close()

Crawler()