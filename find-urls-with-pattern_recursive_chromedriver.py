# -*- coding: utf-8 -*-
# coding: utf-8

import requests
import re
import xlsxwriter
from bs4 import BeautifulSoup
from urllib.parse import urlparse

import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

class Crawler():
    base = 'https://warrenshea.github.io/'
    start_link = 'https://warrenshea.github.io/'
    pattern_to_match = 'examples'
    pattern_to_exclude = [
    ]
    visited_links = []
    non_pattern_links = []

    #chromedriver = '/usr/local/bin/chromedriver' #macos
    chromedriver = 'E:/chromedriver' #windows
    driver = webdriver.Chrome(chromedriver)

    def __init__(self):
        self.crawl_url(self.start_link)
        self.print_visited_links()
        self.driver.close()

    def filter_link(self, url):

        #url = urlparse(url).path # Get the path
        url = self.base + urlparse(url).path
        path = urlparse(url).path # Get the path

        # If it's a file or popup or javascript function
        if path.find('.') != -1 or url.find('popup') != -1 or url.find('javascript') != -1:
            return

        # url = url.replace('//','/') # Replace any accidental // with /
        if not url.endswith('/'): # Add Trailing Slash for consistency
            url = url + '/'

        print(url,self.base + self.pattern_to_match)
        if url.find(self.base + self.pattern_to_match) != -1: # URL must match pattern_to_match
            return url
        else:
            return

    def crawl_url(self, url):
        print('Crawled url: ' + url)

        filtered_links = []
        all_links_raw = []

        self.visited_links.append(url)
        self.driver.get(url)
        page = self.driver.page_source
        soup = BeautifulSoup(page, 'html.parser')

        for anchor in soup.find_all('a', href=True):
            #print(anchor['href'])
            all_links_raw.append(anchor['href'])

        for raw_link in all_links_raw:
            self.non_pattern_links.append(raw_link)
            link = self.filter_link(raw_link)
            # if (link is not None):
            #     print(link)
            if (link is not None) and link not in self.visited_links:
                # print(link)
                filtered_links.append(link)

        for next_url in filtered_links:
            full_url = str(next_url)
            if full_url not in self.visited_links:
                self.crawl_url(full_url)

    def getEnglish(self, url):
        self.driver.get(url)
        page = self.driver.page_source
        soup = BeautifulSoup(page, 'html.parser')

        for htmlnode in soup.select('link[hreflang="en"]'):
            return htmlnode['href']

    def getFrench(self, url):
        self.driver.get(url)
        page = self.driver.page_source
        soup = BeautifulSoup(page, 'html.parser')

        for htmlnode in soup.select('link[hreflang="fr"]'):
            return htmlnode['href']

    def print_visited_links(self):
        # print('************');
        workbook = xlsxwriter.Workbook('find-urls-with-pattern_recursive_chromedriver.xlsx')
        worksheet = workbook.add_worksheet()
        cell_format = workbook.add_format({'bold': True, 'font_color': 'white', 'bg_color': 'black'})
        worksheet.set_column('A:A', 60)
        worksheet.set_column('B:B', 60)
        worksheet.set_column('C:C', 60)
        worksheet.set_column('D:D', 60)

        worksheet.write(0,0,'Crawled URLs FR', cell_format)
        row = 1
        column = 0
        for item in sorted(self.visited_links):
            worksheet.write(row,column,item)
            row += 1

        worksheet.write(0,1,'Crawled URLs EN', cell_format)
        row = 1
        column = 1
        for item in sorted(self.visited_links):
            french_url = self.getEnglish(item)
            worksheet.write(row,column,french_url)
            row += 1
            print ('EN : {}'.format(item))
            print ('FR : {}'.format(french_url))

        worksheet.write(0,2,'All Links from Crawled pages (Unique)', cell_format)
        row = 1
        column = 2
        for item in sorted(list(set(self.non_pattern_links))):
            worksheet.write(row,column,item)
            row += 1

        worksheet.write(0,3,'All Links from Crawled pages', cell_format)
        row = 1
        column = 3
        for item in sorted(self.non_pattern_links):
            worksheet.write(row,column,item)
            row += 1
        workbook.close()

Crawler()