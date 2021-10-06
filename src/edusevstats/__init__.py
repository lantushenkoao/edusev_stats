from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager


import logging
import logging.config
import os.path

from crawler import Crawler

loggerCfgFile = 'logging.conf'

if __name__ == '__main__':
    pass

if os.path.isfile(loggerCfgFile):
    logging.config.fileConfig(loggerCfgFile)


crawler = Crawler
df = crawler.crawl(crawler)
df.to_excel("SchoolsLoad.xlsx")
