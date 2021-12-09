import logging
import re

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

URL_SCHOOL_LIST = "https://eduface.ru/sites/list/region/1"
XPATH_SCHOOL_LINK = "//h3[starts-with(text(),'Школы (')]/..//div[@class='accordion-style4-wraplink']//a[contains(@href,'edusev.ru')]"
XPATH_SCHOOL_TITLE = "span"
URL_CLASSES_LIST = "{url}vacant"
XPATH_CLASSES_LIST = "//h2[text()='Классы']/..//a[starts-with(text(), 'Класс ')]"
XPATH_CLASS_FILLING_ACTUAL="//div[starts-with(text(), 'Фактически обучаются')]/span"
XPATH_CLASS_FILLING_EXPECTED="//div[starts-with(text(), 'Нормативная наполняемость класса')]/span"
class Crawler:
    logger = []
    driver = []
    

    def crawl(self):
        self.logger = logging.getLogger("crawler")
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        #df = pd.DataFrame(columns=["school_id", "school", "class", "actual", "expected"])
        df = pd.DataFrame()
        #schools = self.loadSchools(self)[:3]
        schools = self.loadSchools(self)
        for school in schools:
            self.logger.info("Processing %s" % (school["title"]))
            classes = self.loadClasses(self, school["url"])
            for clazz in classes:
                classData = self.loadClassData(self, clazz["url"])
                self.logger.debug("Class: %s. Actual %s, Expected %s" % (clazz["title"], classData["actual"], classData["expected"]))
                # newRow = [school["id"], school["title"], clazz["title"], 
                #             classData["actual"], classData["expected"]];
                # df = df.append(newRow)
                df = df.append({"school_id":school["id"], "school": school["title"], "class": clazz["title"], 
                           "actual": classData["actual"], "expected": classData["expected"]}, ignore_index=True)
        self.logger.info("Crawling completed")
        return df
            
            
    def loadSchools(self):
        self.logger.info("Loading schools list")
        self.driver.get(URL_SCHOOL_LIST)
        result = []
        for school in self.driver.find_elements(By.XPATH, XPATH_SCHOOL_LINK):
            url = school.get_attribute("href")
            id = url.replace("http://","").replace("https://","").replace(".edusev.ru", "").replace("/","")
            result.append({ "id": id, "title" : school.get_attribute("innerText"), "url": url})
        return result
    
    def loadClasses(self, url):
        self.driver.get(URL_CLASSES_LIST.format(url=url))
        classes = self.driver.find_elements(By.XPATH, XPATH_CLASSES_LIST)
        result = []
        for clazz in classes:
            href = clazz.get_attribute("href")
            title = clazz.text
            result.append({"title": title, "url": href})
            self.logger.info("Loaded class " + title)
        return result;
    
    def loadClassData(self, url):
        self.driver.get(url)
        fillingExpected = self.driver.find_element(By.XPATH, XPATH_CLASS_FILLING_EXPECTED).text
        fillingActual = self.driver.find_element(By.XPATH, XPATH_CLASS_FILLING_ACTUAL).text
        return {"expected": fillingExpected, "actual": fillingActual}
