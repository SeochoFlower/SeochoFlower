import pymysql
from flask import Flask, request, jsonify, render_template
import time
from selenium import webdriver
from pyvirtualdisplay import Display

# Python 과 MySQL 연결하기
db = pymysql.connect(host='host-endpoint', port=3306, user='ukiiing00', passwd='****', db='ai_college', charset="utf8")
cursor = db.cursor() # 커서 클래스 호출

conn = Flask(__name__)
display = Display(visible=0, size=(1024,768))
display.start()
with webdriver.Chrome('/home/ukiiing00/chromedriver') as driver:
#driver = webdriver.Chrome('C:\driver\chromedriver.exe')
    driver.get('https://flower.at.or.kr/real/real2.do')

    print(driver.title)
    print(driver.current_url)
    print("실시간 경매 데이터")

    string_list = []
    full_list = []
    while True:

        tbody = driver.find_element_by_tag_name('tbody')
        row_list = tbody.find_elements_by_tag_name('tr')


        for row in row_list:
            string = row.text
            # 문자열 string을 split()하여 리스트로 변환
            string_list = string.split()
            full_list.append(string_list)

        try:
            driver.find_element_by_id('next_jqGridPager').click()

        except:
            break

full_list = [v for v in full_list if v]

for lis in full_list :
    sql = """insert into realtime_flower (poomname, goodname, lvname, qty, cost) VALUES( '%s', '%s', '%s', %s, %s)""" % \
        (lis[1], lis[2], lis[3], lis[4], int(lis[5].replace(',','')) )
    cursor.execute(sql)
    db.commit()

