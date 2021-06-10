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
    crawl_page_en = "https://warrenshea.github.io/"
    crawl_page_fr = "https://warrenshea.github.io/"

    #chromedriver = '/usr/local/bin/chromedriver' #macos
    chromedriver = 'E:/chromedriver' #windows
    driver = webdriver.Chrome(chromedriver)

    def __init__(self):
        workbook = xlsxwriter.Workbook('single-page-audit_chromedriver.xlsx')
        self.crawl_url(workbook, self.crawl_page_en, 'en')
        self.crawl_url(workbook, self.crawl_page_fr, 'fr')
        workbook.close()
        self.driver.close()

    def crawl_url(self, workbook, crawl_page, lang):
        worksheet = workbook.add_worksheet(lang)

        cell_format_left = workbook.add_format({'bold': True, 'font_color': 'white', 'bg_color': 'black'})
        cell_format_right = workbook.add_format({'bold': True, 'font_color': 'white', 'bg_color': 'black', 'align': 'right'})
        worksheet.set_column('A:A', 20)
        worksheet.set_column('B:B', 250)
        worksheet.write(0,0,'Crawled URL:', cell_format_right)
        worksheet.write(0,1,crawl_page, cell_format_left)
        link = 1
        row = 1
        col = 0

        self.driver.get(crawl_page)
        page = self.driver.page_source
        soup = BeautifulSoup(page, 'html.parser')

        for anchor in soup.body.find_all('a'):
            worksheet.write(row,0,'Link #', cell_format_right)
            worksheet.write(row,1,link,workbook.add_format({'align': 'left'}))
            row += 1

            worksheet.write(row,0,'text', cell_format_right)
            worksheet.write(row,1,anchor.text)
            row += 1

            worksheet.write(row,0,'href', cell_format_right)
            if anchor.has_attr('href'):
                worksheet.write(row,1,anchor['href'])
            row += 1

            worksheet.write(row,0,'target', cell_format_right)
            if anchor.has_attr('target'):
                worksheet.write(row,1,anchor['target'])
            row += 1

            worksheet.write(row,0,'aria-label', cell_format_right)
            if anchor.has_attr('aria-label'):
                worksheet.write(row,1,anchor['aria-label'])
            row += 1

            # worksheet.write(row,0,'data-ana', cell_format_right)
            # if anchor.has_attr('data-ana'):
            #     worksheet.write(row,1,anchor['data-ana'])
            # row += 1

            # worksheet.write(row,0,'data-meta', cell_format_right)
            # if anchor.has_attr('data-meta'):
            #     worksheet.write(row,1,anchor['data-meta'])
            # row += 1

            worksheet.write(row,0,'anchor code', cell_format_right)
            worksheet.write(row,1,anchor.prettify())
            row += 2
            link += 1

Crawler()