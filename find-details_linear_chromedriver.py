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

PYTHONHTTPSVERIFY=0

class Crawler():
    crawl_list = [
        "https://warrenshea.github.io/",
    ]

    # One of these must be active

    # crawl = "canonical"
    # crawl = "alternatelang"
    crawl = "find-anchors"
    # crawl = "find-pdfs"
    # crawl = "get-status-code"
    # crawl = "find-forms"
    # crawl = "find-iframes"

    needles = [
        "examples"
        # "/"
        # ".pdf",
        # ".PDF"
        # "pdf",
        # "PDF"
        # "googletagmanager",
    ]

    #chromedriver = '/usr/local/bin/chromedriver' #macos
    chromedriver = 'E:/chromedriver' #windows
    driver = webdriver.Chrome(chromedriver)

    def __init__(self):
        self.crawl_url(self.crawl_list)
        self.driver.close()

    def has_needle(self, anchor):
        #anchor = urlparse(anchor).path
        for needle in self.needles:
            if needle in anchor:
                return True

    def get_status_code(self, path="/"):
        """ This function retreives the status code of a website by requesting
            HEAD data from the host. This means that it only requests the headers.
            If the host cannot be reached or something else goes wrong, it returns
            None instead.
        """
        try:
            print(path)
            r = requests.get(path, verify=False)
            # prints the int of the status code. Find more at httpstatusrappers.com :)
            return r.status_code
        except requests.ConnectionError:
            print("failed to connect")

    def crawl_url(self, url_list):
        if self.crawl == "canonical":
            workbook = xlsxwriter.Workbook('find-details_canonical.xlsx')
        elif self.crawl == "alternatelang":
            workbook = xlsxwriter.Workbook('find-details_alternatelang.xlsx')
        elif self.crawl == "find-anchors":
            workbook = xlsxwriter.Workbook('find-details_anchors.xlsx')
        elif self.crawl == "find-pdfs":
            workbook = xlsxwriter.Workbook('find-details_pdfs.xlsx')
        elif self.crawl == "find-forms":
            workbook = xlsxwriter.Workbook('find-details_forms.xlsx')
        elif self.crawl == "find-iframes":
            workbook = xlsxwriter.Workbook('find-details_iframes.xlsx')
        elif self.crawl == "get-status-code":
            workbook = xlsxwriter.Workbook('find-details_get-status-code.xlsx')

        worksheet = workbook.add_worksheet()
        cell_format = workbook.add_format({'bold': True, 'font_color': 'white', 'bg_color': 'black'})
        worksheet.set_column('A:A', 60)
        worksheet.write(0,0,'Crawled URLs', cell_format)
        if self.crawl == "canonical":
            worksheet.set_column('B:B', 30)
            worksheet.set_column('C:C', 30)
            worksheet.set_column('D:D', 30)
            worksheet.write(0,1,'Canonical URL', cell_format)
        elif self.crawl == "alternatelang":
            worksheet.set_column('B:B', 10)
            worksheet.set_column('C:C', 30)
            worksheet.set_column('D:D', 10)
            worksheet.set_column('E:E', 30)
            worksheet.set_column('F:F', 10)
            worksheet.set_column('G:G', 30)
            worksheet.set_column('H:H', 10)
            worksheet.set_column('I:I', 30)
            worksheet.write(0,1,'lang', cell_format)
            worksheet.write(0,2,'href', cell_format)
            worksheet.write(0,3,'lang', cell_format)
            worksheet.write(0,4,'href', cell_format)
            worksheet.write(0,5,'lang', cell_format)
            worksheet.write(0,6,'href', cell_format)
            worksheet.write(0,7,'lang', cell_format)
            worksheet.write(0,8,'href', cell_format)
        elif self.crawl == "find-anchors":
            worksheet.set_column('B:B', 30)
            worksheet.write(0,1,'anchor', cell_format)
        elif self.crawl == "find-forms":
            worksheet.set_column('B:B', 30)
            worksheet.set_column('C:C', 30)
            worksheet.set_column('D:D', 30)
            worksheet.set_column('E:E', 30)
            worksheet.write(0,1,'name', cell_format)
            worksheet.write(0,2,'action', cell_format)
            worksheet.write(0,3,'method', cell_format)
            worksheet.write(0,4,'id', cell_format)
        elif self.crawl == "find-iframes":
            worksheet.set_column('B:B', 30)
            worksheet.write(0,1,'src', cell_format)
        elif self.crawl == "get-status-code":
            worksheet.set_column('B:B', 30)
            worksheet.write(0,1,'src', cell_format)
        row = 1
        col = 0

        for url in url_list:
            self.driver.get(url)
            print(url)
            page = self.driver.page_source
            soup = BeautifulSoup(page, 'html.parser')

            if self.crawl == "canonical":
                for anchor in soup.find_all('link'):
                    if anchor.has_attr('rel'):
                        if anchor['rel'][0] == "canonical":
                            worksheet.write(row,0,url)
                            worksheet.write(row,1,anchor['href'])
                            row += 1
            elif self.crawl == "alternatelang":
                worksheet.write(row,0,url)
                col = 1
                for anchor in soup.find_all('link'):
                    if anchor.has_attr('rel'):
                        if anchor['rel'][0] == "alternate":
                            if anchor.has_attr('hreflang'):
                                worksheet.write(row,col,anchor['hreflang'])
                                worksheet.write(row,col+1,anchor['href'])
                    col += 2
                row += 1
            elif self.crawl == "find-anchors":
                col = 1
                if (soup.body):
                    for anchor in soup.body.find_all('a', href=True):
                        if self.has_needle(anchor['href']):
                            print(anchor['href'])
                            worksheet.write(row,0,url)
                            worksheet.write(row,col,anchor['href'])
                            row += 1
            elif self.crawl == "find-pdfs":
                col = 1
                for anchor in soup.find_all('a', href=True):
                    if self.has_needle(anchor['href']):
                        worksheet.write(row,0,url)
                        worksheet.write(row,col,anchor['href'])
                        row += 1
                for option in soup.find_all('option', value=True):
                    if self.has_needle(option['value']):
                        worksheet.write(row,0,url)
                        worksheet.write(row,col,option['value'])
                        row += 1
            elif self.crawl == "find-forms":
                for form in soup.body.find_all('form'):
                    col = 1
                    worksheet.write(row,0,url)
                    print(url);
                    if form.has_attr('name'):
                        worksheet.write(row,col,form['name'])
                        print(form['name']);
                    if form.has_attr('action'):
                        worksheet.write(row,col+1,form['action'])
                        print(form['action']);
                    if form.has_attr('id'):
                        worksheet.write(row,col+2,form['id'])
                        print(form['id']);
                    if form.has_attr('method'):
                        worksheet.write(row,col+3,form['method'])
                        print(form['method']);
                    row += 1
            elif self.crawl == "find-iframes":
                for iframe in soup.body.find_all('iframe', src=True):
                    col = 1
                    worksheet.write(row,0,url)
                    if not self.has_needle(iframe['src']):
                        worksheet.write(row,col,iframe['src'])
                        print('URL: ' + url);
                        print(iframe['src']);
                        row += 1
            elif self.crawl == "get-status-code":
                worksheet.write(row,0,url)
                worksheet.write(row,1,self.get_status_code(url))
                row += 1
        workbook.close()

Crawler()