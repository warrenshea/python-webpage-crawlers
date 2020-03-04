# -*- coding: utf-8 -*-
# coding: utf-8

import requests
import re
import xlsxwriter
from bs4 import BeautifulSoup
from urlparse import urlparse

import os  
from selenium import webdriver
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options  

class Crawler():
    base = 'https://www.domain.com'
    start_link = 'https://www.domain.com/home/'
    pattern_to_match = '/home'
    visited_links = []
    non_pattern_links = []

    # chrome_options = Options()  
    # chrome_options.add_argument("--headless")  
    # chrome_options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'

    chromedriver = '/usr/local/bin/chromedriver'
    driver = webdriver.Chrome(chromedriver)

    def __init__(self):
        self.crawl_url(self.start_link)
        self.print_visited_links()
        self.driver.close()

    def filter_link(self, url):
        url = urlparse(url).path # Get the path

        # If it's a file or popup or javascript function
        if url.find('.') != -1 or url.find('popup(') != -1 or url.find('javascript(') != -1:
            return
        
        url = url.replace('//','/') # Replace any accidental // with /
        if not url.endswith('/'): # Add Trailing Slash for consistency
            url = url + '/'

        if url.find(self.pattern_to_match) != -1: # URL must match pattern_to_match
            return url
        else:
            return

    def crawl_url(self, url):
        print('Crawled url: ' + url)

        filtered_links = []
        all_links_raw = []

        self.visited_links.append(url)

        self.driver.implicitly_wait(50000)
        self.driver.get(url)
        self.driver.implicitly_wait(50000)
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
                print(link)
                filtered_links.append(link)

        for next_url in filtered_links:
            full_url = str(self.base + next_url)
            if full_url not in self.visited_links:
                self.crawl_url(full_url)



    def getFrench(self, url):
        self.driver.implicitly_wait(50000)
        self.driver.get(url)
        self.driver.implicitly_wait(50000)
        page = self.driver.page_source
        soup = BeautifulSoup(page, 'html.parser')

        for htmlnode in soup.select('link[hreflang="fr"]'):
            return htmlnode['href']

    def print_visited_links(self):
        print('************');

        workbook = xlsxwriter.Workbook('results.xlsx')
        worksheet = workbook.add_worksheet()
        cell_format = workbook.add_format({'bold': True, 'font_color': 'white', 'bg_color': 'black'})

        worksheet.write(0,0,'Crawled URLs EN', cell_format)
        row = 1
        column = 0
        for item in sorted(self.visited_links):
            worksheet.write(row,column,item)
            row += 1

        worksheet.write(0,1,'Crawled URLs FR', cell_format)
        row = 1
        column = 1
        for item in sorted(self.visited_links):
            french_url = self.getFrench(item)
            worksheet.write(row,column,french_url)
            row += 1
            print 'EN : {}'.format(item)
            print 'FR : {}'.format(french_url)

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