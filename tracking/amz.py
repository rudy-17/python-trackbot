import os
import re
import sys
import time
import random
import hashlib
import smtplib
import argparse
import datetime
import itertools
import subprocess
import csv
import memcache
from bs4 import BeautifulSoup
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from collections import defaultdict

class AmzChromeDriver(object):
    """ Replacement driver to login to Amazon and download URLs using the Selenium ChromeDriver. """
    def __init__(self):
        from selenium import webdriver
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--no-sandbox')
        chrome_options.binary_location = '/app/.apt/usr/bin/google-chrome'
        # from pyvirtualdisplay import Display
        # display = Display(visible=0, size=(1024, 768))
        # display.start()
        self.driver = webdriver.Chrome('/app/.chromedriver/bin/chromedriver', chrome_options=chrome_options, service_args=['--verbose', '--log-path=/tmp/chromedriver.log'])
        self.driver.implicitly_wait(30)
        #'/usr/local/bin/chromedriver'
        #/app/.chromedriver/bin/chromedriver

    def login(self, email, password):
        driver = self.driver
        driver.get("https://www.amazon.com")
        #nav-link-yourAccount > span.nav-line-1
        driver.find_element_by_css_selector("#nav-link-accountList > span.nav-line-1").click()
        #driver.find_element_by_css_selector("#nav-signin-tooltip > a.nav-action-button").click()
        driver.find_element_by_id("ap_email").clear()
        driver.find_element_by_id("ap_email").send_keys(email)
        #driver.find_element_by_id("continue").click()
        driver.find_element_by_id("ap_password").clear()
        driver.find_element_by_id("ap_password").send_keys(password)
        driver.find_element_by_id("signInSubmit").click()

    def get_url(self, url):
        self.driver.get(url)
        return self.driver.page_source

    def get_url_driver(self, url):
        self.driver.get(url)
        return self.driver

    def clean_up(self):
        self.driver.quit()


class AmzScraper(object):
    base_url = 'https://www.amazon.com'
    start_url = base_url+'/gp/css/history/orders/view.html?orderFilter=year-{yr}&startAtIndex=1000'
    order_url = base_url+'/gp/css/summary/print.html/ref=od_aui_print_invoice?ie=UTF8&orderID={oid}'

    order_date_re = re.compile(r'Order Placed:')
    order_id_re = re.compile(r'orderID=([0-9-]+)')

    def __init__(self, year, user, password, cache_timeout, brcls=AmzChromeDriver):

        self.year = year
        self.mc = memcache.Client(['127.0.0.1:11211'], debug=0)
        self.br = brcls()
        self.cache_timeout = cache_timeout
        self.br.login(user, password)

    def _fetch_url(self, url, use_cache=True):
        key = hashlib.md5(url.encode('utf-8')).hexdigest()
        val = use_cache and self.mc.get(key) or None
        if not val:
            print ('fetching %s from server (with random sleep)' % url)
            val = self.br.get_url(url)
            # wait a little while so we don't spam Amazon
            time.sleep(random.randint(1, 5))
            self.mc.set(key, val, self.cache_timeout)
            from_cache = False
        else:
            print ('using cache for %s' % url)
            from_cache = True
        return val, from_cache

    def get_order_links(self):
        order_links = []
        url = self.start_url.format(yr=self.year)
        for page_num in itertools.count(start=2, step=1):
            html, _ = self._fetch_url(url)
            soup = BeautifulSoup(html, 'lxml')
            links = soup.find_all("a")
            for link in links:
                if "order-details" in str(link.get("href")):
                    order_links.append("https://www.amazon.com"+str(link.get("href")))
            page_links = soup.find_all('a', text=str(page_num))
            if not page_links:
                print ('found no links for page_num=%s; assuming completion' % page_num)
                break
            url = self.base_url + page_links[0]['href']
        return order_links

    def run(self):
        complete_data = []
        def fn(element, key=0):
            if len(element) > 0:
                return element[key].text
            else:
                return ''

        order_links = self.get_order_links()
        if len(order_links)!=0:
            def fn(element, key=0):
                if len(element) > 0:
                    return element[key].text
                else:
                    return ''
            del order_links[-1]
            for link in order_links:
                data = {}
                driver=self.br.get_url_driver(link)
                element = driver.find_elements_by_xpath('.//*[@class="order-date-invoice-item"]')
                data['order-data'] = fn(element)
                data['order-number'] = element[1].text[7:]
                element = driver.find_elements_by_xpath('.//*[@class="a-box-inner"]/div[1]/div[1]/div[1]/span')
                data['order-status'] = fn(element)
                element = driver.find_elements_by_xpath('.//*[@class="displayAddressDiv"]/ul[1]')
                data['shipping-address'] = fn(element)
                element = driver.find_elements_by_xpath('.//*[@class="a-section a-spacing-none"]/div[1]')
                data['payment-method'] = fn(element)
                element = driver.find_elements_by_xpath('.//*[@class="a-fixed-left-grid-col a-col-right"]/div[1]/a[1]')
                data['product-name'] = fn(element)
                element = driver.find_elements_by_xpath('.//*[@class="yo-critical-feature"]')
                if len(element) > 0:
                    data['product-image'] = element[0].get_attribute('src')

                import time
                try:
                    if data['order-status'] != '':
                        track_url = "https://www.amazon.com/progress-tracker/package/ref=oh_aui_hz_st_btn?_encoding=UTF8&itemId=qjmpotplkpttq&orderId="+data['order-number']
                        driver=self.br.get_url_driver(track_url)
                        driver.find_element_by_css_selector("#deliveredAddress > .a-row > .a-declarative").click()
                        time.sleep(5)
                        element = driver.find_elements_by_xpath('.//*[@class="a-row tracking-event-trackingId-text"]/h4[1]')[0].text
                        data['trackingID'] = element
                        columns = driver.find_elements_by_xpath('.//*[@class="a-container"]/div')
                        temp = defaultdict(list)
                        for i in range(2, len(columns)-1):
                            rows = columns[i].find_elements_by_xpath(".//*[@class='a-row tracking-event-date-header']")
                            date = fn(rows)
                            rows = columns[i].find_elements_by_xpath(".//*[@class='a-row a-spacing-large a-spacing-top-medium']")
                            for each in rows:
                                left = each.find_elements_by_xpath(".//*[@class='a-column a-span3 tracking-event-time-left']")[0].text
                                right = each.find_elements_by_xpath(".//*[@class='a-column a-span9 tracking-event-time-right a-span-last']")[0].text
                                temp[date].append([left, right])
                        data['tracking-status'] = temp
                        complete_data.append(data)
                except:
                    print("Not Possible")
                    print(data)
                print(data)
        return complete_data

    def main(user, password, year):
        years = year
        for year in years:
            data = AmzScraper(year=year, user = user, password = password, cache_timeout=21600).run()
        return data
