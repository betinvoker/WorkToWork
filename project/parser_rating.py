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

    pagination = driver.find_element_by_class_name('pagination')
    pages = pagination.find_elements_by_class_name('text')

    for page in pages:
        block = driver.find_element_by_class_name('main')
        universiteties = block.find_elements_by_class_name('-rating')
        
        for university in universiteties:
            position = university.find_element_by_class_name('position')
            name = university.find_element_by_class_name('name')

            print("%s|%s\n" % (position.text, name.text))

        driver.get("https://academia.interfax.ru/ru/ratings/?rating=1&year=2020&page=" + page.text)




if __name__ == "__main__":
    main()