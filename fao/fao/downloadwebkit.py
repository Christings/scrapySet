from selenium import webdriver
from scrapy.http import HtmlResponse
import time


class WebkitDownloader(object):
    # 通过selenium打开chrome内核，从而获得网页加载后的源代码。
    def process_request(self, request, spider):
        if spider.name == "faocountries":   # 注意：之前scrapy和senelium一直没连接起来，是因为spider.name写的是spider。
            print("chrome is starting...")
            browser = webdriver.Chrome(
                executable_path="C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")
            # browser=webdriver.PhantomJS( executable_path=r'E:\Program Files\phantomjs-2.1.1-windows\bin\phantomjs.exe')
            browser.get(request.url)
            time.sleep(20)
            # body=browser.find_element_by_id('groups-list')
            # body_child=body.get_attribute('innerHTML')
            body = browser.page_source
            print("访问的url：", request.url)
            return HtmlResponse(browser.current_url, body=body, encoding='utf-8', request=request)
        else:
            return
