from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

import logging
import logging.config
import os.path

ARTICLE_PATH = "article_d3.html"
SUBST_START = "//jsonDataSubstitutionStart"
SUBST_END = "//jsonDataSubstitutionEnd"

from crawler import Crawler

loggerCfgFile = 'logging.conf'

if __name__ == '__main__':
    pass

if os.path.isfile(loggerCfgFile):
    logging.config.fileConfig(loggerCfgFile)
logger = logging.getLogger("main")


logger.info("Crawling")
crawler = Crawler
df = crawler.crawl(crawler)
# df.to_excel("SchoolsLoad.xlsx")
# ##json = df.to_json(path_or_buf="SchoolsLoad.json", orient="table")
json = df.to_json(orient="table")
#json = open("SchoolsLoad.json", "r").read()

# Read in the file
with open(ARTICLE_PATH, 'r') as file :
    article = file.read()

# Replace the target string
article_start = article[:article.index(SUBST_START)+len(SUBST_START)]
article_end = article[article.index(SUBST_END):]

# Write the file out again
with open(ARTICLE_PATH, 'w') as file:
    file.truncate(0)
    file.write(article_start + "\n jsonDataRaw = " + json + "\n" + article_end)
    
logger.info("JSON data written to HTML article " + ARTICLE_PATH)