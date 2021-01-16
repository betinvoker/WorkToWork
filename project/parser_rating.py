from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import sqlite3
import os
import time

path = r"chromedriver.exe"
driver = webdriver.Chrome(executable_path=path)

def main():
    driver.get("https://academia.interfax.ru/ru/ratings/?rating=1&year=2020&page=1")

    block = driver.find_element_by_class_name('main')
    universiteties = block.find_elements_by_class_name('-rating')
    
    i = 1

    for university in universiteties:
        position = university.find_element_by_class_name('position')
        name = university.find_element_by_class_name('name')
        link = university.find_element_by_xpath('/html/body/div[1]/div[4]/div/section/main/div/div[%s]/a' % i)

        print("%s|%s|%s\n" % (position.text, name.text, link.get_attribute("href")))

        i += 1

if __name__ == "__main__":
    main()