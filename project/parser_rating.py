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

conn = sqlite3.connect('db.sqlite3')
#   Создать соединение с базой
cursor = conn.cursor()

def main():
    driver.get("https://academia.interfax.ru/ru/ratings/?rating=0&page=1")
    #   Удалить все университеты из базы
    delete_universities()
    #   Заполнение таблицы
    parse_universities()
    #   Закрыть браузер после выполнения
    driver.close()

#   Заполнение таблицы
def parse_universities():
    nav = driver.find_element_by_class_name('pagination')
    pages = nav.find_elements_by_class_name('page')

    for page in pages:
        block = driver.find_element_by_class_name('main')
        universiteties = block.find_elements_by_class_name('-rating')

        if pages.index(page) > 1:
            for university in universiteties:
                dict_university = take_data_university(university, universiteties.index(university) + 1)
                adding_universities(dict_university.get('name'), dict_university.get('link'))
                print("%s|%s\n" % (dict_university.get('name'), dict_university.get('link')))
            driver.get("https://academia.interfax.ru/ru/ratings/?page=%s&rating=0&year=2020" % str(pages.index(page)))
            time.sleep(5)

    conn.commit()

#   Взять из блока данные об университете
def take_data_university(university, index):
    name = university.find_element_by_class_name('name')
    link = university.find_element_by_xpath('/html/body/div[1]/div[4]/div/section/main/div/div[%s]/a' % index)

    dict_university = {'name' : name.text, 'link' : link.get_attribute("href")}

    return dict_university

#   Добавить университет в базу
def adding_universities(name, link):
    cursor.execute("INSERT INTO search_reviews_ratings(name, link) VALUES (?,?)", (name, link))

#   Удалить все университеты из базы
def delete_universities():
    cursor.execute("DELETE FROM search_reviews_ratings")

if __name__ == "__main__":
    main()