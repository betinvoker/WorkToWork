from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
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
    #   Проверить и заполнить таблицу Universities.
    changing_the_table_universities()
    #   Проверить и заполнить таблици Opinions. 
    filling_in_the_table_opinions()
    #   Закрыть браузер после выполнения
    driver.close()

#   Проверить таблицу Universities на заполненность и заполнить.
def changing_the_table_universities():
    #   Главная страница сайта
    driver.get("https://tabiturient.ru/")
    #   Нажимать на кнопку загрузить еще, пока она существует на странице
    click_btn('mobpadd20', '/html/body/div[1]/div[2]/div[1]/div/div[5]')
    #   Найти общее количество университетов
    all_universities = len(driver.find_elements_by_class_name('mobpadd20'))
    #   Берем количество записей из таблицы Universities и присваиваем его переменной
    cursor.execute("SELECT COUNT(*) FROM search_reviews_universities")
    count_universities = int(cursor.fetchone()[0])
    #   Условия при которых будут собираться данные
    conditional_actions_of_universities(count_universities, all_universities)

#   Проверить таблицу Opinions на заполненность и заполнить.
def filling_in_the_table_opinions():
    #   Взять из базы список университетов
    cursor.execute("SELECT * from search_reviews_universities")
    all_universities = cursor.fetchall()
    #   Перебрать все университеты по списку
    for university in all_universities:
        #   Cтраница Университета
        driver.get(university[3])
        #   Нажимать на кнопку загрузить еще, пока она существует на странице
        click_btn('mobpadd10', '/html/body/div[1]/div[2]/div[1]/div/div[7]')
        time.sleep(5)
        #   Найти общее количество отзывов
        all_opinions = int(len(list(driver.find_elements_by_class_name('mobpadd20-2'))))
        #   Берем количество записей из таблицы Opinions и присваиваем его переменной
        cursor.execute("SELECT search_reviews_universities.id, COUNT(search_reviews_opinions.university_id) FROM search_reviews_universities LEFT JOIN search_reviews_opinions ON search_reviews_universities.id = search_reviews_opinions.university_id WHERE search_reviews_universities.id = "  + str(university[0]) + " GROUP BY search_reviews_universities.id")
        count_opinions = int(cursor.fetchone()[1])
        #   Условия при которых будут собираться данные
        conditional_actions_of_opinions(count_opinions, all_opinions, university)

    print("----- Заполнение таблицы завешено -----\n")

#   Условия при которых будут собираться данные
def conditional_actions_of_universities(count_universities, all_universities):
    print("----- Таблица Universities содержит - " + str(count_universities) + " записей из "+ str(all_universities) +" -----\n")

    if count_universities == 0 and all_universities != 0:
        print("--- В таблице нет записей, происодит заполнение таблицы.\n")
        parse_list_of_universities()
    elif all_universities == 0:
        print("--- На сайте нет записей об университетах.\n")
    elif count_universities < all_universities:
        #   Пока не придумал, что должно тут выводиться
        print("--- Записей в таблице меньше, чем на сайте.\n")
    elif count_universities > all_universities:
        print("--- В таблице больше записей чем на сайте, это странно!\n")
    elif count_universities == all_universities:
        print("--- Все хорошо, обновлений нет.\n")

    print("----- Заполнение таблицы завешено -----\n")

#   Условия при которых будут собираться данные
def conditional_actions_of_opinions(count_opinions, all_opinions, university):
    print("----- " + str(university[1]) + " | Кол-во отзывов - " + str(count_opinions) + "/" + str(all_opinions) + " -----\n")

    if count_opinions == 0 and all_opinions != 0:
        print("--- В таблице нет записей, происодит заполнение таблицы.\n")
        parse_list_of_opinions(university[0])
    elif all_opinions == 0:
        print("--- На сайте нет отзывов об " + str(university[1]) + ".\n")
    elif count_opinions < all_opinions:
        #   Пока не придумал, что должно тут выводиться
        print("--- Записей в таблице меньше, чем на сайте.\n")
    elif count_opinions > all_opinions:
        print("--- В таблице больше записей чем на сайте, это странно!\n")
    elif count_opinions == all_opinions:
        print("--- Все хорошо, обновлений нет.\n")

#   Парсить данные об университетах со страницы
def parse_list_of_universities():  
    block = driver.find_element_by_id('resultdiv0')
    all_universities = block.find_elements_by_class_name('mobpadd20')

    index = 1
    #   Цикл сбора данных и записи данных об университете
    for university in all_universities:
        #   Взять из блока данные об университете
        dict_university = take_data_university(university, index)
        
        print(dict_university.get('abbreviation') + " | " + dict_university.get('full_name') + " | " + dict_university.get('link') + " | " + dict_university.get('logo') + "\n")
        adding_universities(dict_university.get('abbreviation'), dict_university.get('full_name'), dict_university.get('link'), dict_university.get('logo'))

        dict_university.clear()
        index += 1
    #   Сохранить изменения в базе
    conn.commit()

#   Парсить данные с отзывами об университете
def parse_list_of_opinions(university):
    block = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div[5]')
    all_opinions = reversed(block.find_elements_by_class_name('mobpadd20-2'))

    index = 1
    #   Цикл сбора данных и записи данных отзыва
    for opinion in all_opinions:
        #   Нажимать на ссылку "Показать полностью..."
        click_on_show_link(opinion, '/html/body/div[1]/div[2]/div[1]/div/div[5]/div[' + str(index) + ']/div[1]/div[2]/b')
        #   Взять из блока данные об отзыве
        dict_opinion = take_data_opinion(university, opinion, index)

        print(dict_opinion.get('text') + " | " + dict_opinion.get('date_opinion') + " | " + dict_opinion.get('status') + " | " + dict_opinion.get('id_university') + "\n")
        adding_opinions(dict_opinion.get('text'), dict_opinion.get('date_opinion'), dict_opinion.get('status'), dict_opinion.get('id_university'))
        
        dict_opinion.clear()
        index += 1
    #   Сохранить изменения в базе
    conn.commit()

#   Взять из блока данные об университете
def take_data_university(university, index):
    abbreviation = university.find_element_by_class_name('font3')
    full_name = university.find_element_by_class_name('font2')
    link = university.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div[2]/div[' + str(index) + ']/table[2]/tbody/tr[2]/td/a[3]')
    logo = university.find_element_by_class_name('vuzlistimg')

    dict_university = {'abbreviation' : abbreviation.text, 'full_name' : full_name.text, 'link' : link.get_attribute("href"), 'logo' : logo.get_attribute("src")[31:]}

    return dict_university

#   Взять из блока данные об отзыве
def take_data_opinion(university, opinion, index):
    text = opinion.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div[5]/div[' + str(index) + ']/div[1]/div[2]')
    date_opinion = opinion.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div[5]/div[1]/div[1]/div[1]/div/div[1]/table/tbody/tr/td[2]/table/tbody/tr/td[5]/span[2]')
    status = positive_or_negative_opinions(opinion)
    id_university = str(university)

    dict_opinion = {'text' : text.text, 'date_opinion' : date_opinion.text, 'status' : status, 'id_university' : id_university}

    return dict_opinion

#   Добавить университет в базу
def adding_universities(abbreviated, full_name, link, logo):
    cursor.execute("INSERT INTO search_reviews_universities(abbreviated, name, link, logo) VALUES (?,?,?,?)", 
                        (abbreviated, full_name, link, logo))
       
#   Добавить отзывов об университете в базу
def adding_opinions(text, date_opinion, status, id_university):
    cursor.execute("INSERT INTO search_reviews_opinions(text, date_opinion, status, university_id) VALUES (?,?,?,?)", 
                        (text, date_opinion, status, id_university))

#   Нажимать на кнопку загрузить еще, пока она существует на странице
def click_btn(data_block, button):
    while check_exists_by_class_name(data_block) == True:
        btn = driver.find_element_by_xpath(button)
        if btn.is_displayed():
            btn.click()
            time.sleep(5)
        else:
            break

#   Нажимать на ссылку "Показать полностью..."
def click_on_show_link(opinion, show_full):
    if check_exists_by_xpath(show_full):
        btn = opinion.find_element_by_xpath(show_full)
        driver.execute_script("arguments[0].click();", btn)

#   Узнать, позитивный или негативный отзыв
def positive_or_negative_opinions(opinion):
    picture = opinion.find_element_by_tag_name("img")
    if picture.get_attribute("src") == "https://tabiturient.ru/img/smile2.png":
        return "False"
    else:
        return "True"

#   Проверка элемента на наличие по классу
def check_exists_by_class_name(class_name):
    try:
        driver.find_element_by_class_name(class_name)
    except NoSuchElementException:
        return False
    return True

#   Проверка элемента на наличие по xpath
def check_exists_by_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

if __name__ == "__main__":
    main()