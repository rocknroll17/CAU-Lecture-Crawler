from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
import json

chromedriver ='chromedriver.exe'
driver = webdriver.Chrome(chromedriver)
driver.get('http://rainbow.cau.ac.kr/site/member/login_2')
driver.find_element_by_name("userID").send_keys("여기에 아이디")
driver.find_element_by_name("password").send_keys("여기에 비밀번")
driver.find_element_by_name("password").send_keys(Keys.RETURN)

time.sleep(0.5)
driver.get('http://rainbow.cau.ac.kr/site/reservation/lecture/lectureList?reservegroupid=1&orderby=null&viewtype=L&menuid=001002002&submode=lecture&reserveprogramid=L&searchstatus=&searchlearnsystem=&searchcore=&searchcategorytype=&searchmileagepay=&searchtext=&searchselect=&pagesize=2000&currentpage=1')
res = driver.page_source
driver.quit()
soup = BeautifulSoup(res,"html.parser")

total = soup.select('#searchForm > div.table_style1 > table > tbody > tr:nth-of-type(1) > td:nth-of-type(1)')
total = str(total)
total =int(total[28:32])
json_list = []

for i in range(total):
    num = soup.select('#searchForm > div.table_style1 > table > tbody > tr:nth-of-type('+str(1 + i)+') > td:nth-of-type(1)')
    program = soup.select('#searchForm > div.table_style1 > table > tbody > tr:nth-of-type('+str(1 + i)+') > td:nth-of-type(2) > a')
    apply = soup.select('#searchForm > div.table_style1 > table > tbody > tr:nth-of-type('+str(1 + i)+') > td:nth-of-type(3)')
    lecture = soup.select('#searchForm > div.table_style1 > table > tbody > tr:nth-of-type('+str(1 + i)+') > td:nth-of-type(4)')
    stat = soup.select('#searchForm > div.table_style1 > table > tbody > tr:nth-of-type('+str(1 + i)+') > td:nth-of-type(7) > span')
    
    num = str(num)
    num=int(num[28:32])
    
    program = str(program)
    url = program
    if program[355] == '>':
        program = program[356:-5]
    else:
        program = program[357:-5]


    if '&amp;' in program:
        program = program.replace('&amp;','&')
    if '&lt;' in program:
        program = program.replace('&lt;','<')
    if '&gt;' in program:
        program = program.replace('&gt;','>')
    if '\xa0' in program:
        program = program.replace('\xa0', ' ')

    if url[355] == '"':
        url = url[23:355]
    else:
        url = url[23:354]

    if '&amp;' in url:
        url = url.replace('&amp;','&')

    url = 'http://rainbow.cau.ac.kr' + url
        
    apply = str(apply)
    apply_start = apply[17:29]
    apply_finish = apply[34:44]

    apply_start_year = apply_start[0:4]
    apply_start_month = apply_start[5:7]
    apply_start_day = apply_start[8:10]

    apply_finish_year = apply_finish[0:4]
    apply_finish_month = apply_finish[5:7]
    apply_finish_day = apply_finish[8:10]
    
    lecture = str(lecture)
    lecture_start = lecture[17:29]
    lecture_finish = lecture[34:44]

    lecture_start_year = lecture_start[0:4]
    lecture_start_month = lecture_start[5:7]
    lecture_start_day = lecture_start[8:10]

    lecture_finish_year = lecture_finish[0:4]
    lecture_finish_month = lecture_finish[5:7]
    lecture_finish_day = lecture_finish[8:10]

    stat = str(stat)
    if '신청가능' in stat:
        stat = '신청가능'
    elif '신청마감' in stat:
        stat = '신청마감'
    elif '교육중' in stat:
        stat = '교육중'
    elif '교육종료' in stat:
        stat = '교육종료'
    else:
        stat = 'none'

    if '20' in lecture_start:
        pass
    else:
        lecture_start = 'none'
        
    if '20' in lecture_finish:
        pass
    else:
        lecture_finish = 'none'

    print(num)
    '''
    print(num)
    print(program)
    print(url)
    print(apply_start_year)
    print(apply_start_month)
    print(apply_start_day)
    print(apply_finish_year)
    print(apply_finish_month)
    print(apply_finish_day)
    print(lecture_start_year)
    print(lecture_start_month)
    print(lecture_start_day)
    print(lecture_finish_year)
    print(lecture_finish_month)
    print(lecture_finish_day)
    print(stat,'\n')
    '''

    json_dict = {}
    due = {}
    offered = {}
    due_from = {}
    due_to = {}
    offered_from = {}
    offered_to = {}

    due_from['year'] = apply_start_year
    due_from['month'] = apply_start_month
    due_from['date'] = apply_start_day
    due_to['year'] = apply_finish_year
    due_to['month'] = apply_finish_month
    due_to['date'] = apply_finish_day
    
    offered_from['year'] = lecture_start_year
    offered_from['month'] = lecture_start_month
    offered_from['date'] = lecture_start_day
    offered_to['year'] = lecture_finish_year
    offered_to['month'] = lecture_finish_month
    offered_to['date'] = lecture_finish_day

    due['from'] = due_from
    due['to'] = due_to
    offered['from'] = offered_from
    offered['to'] = offered_to

    json_dict['id'] = num
    json_dict['title'] = program
    json_dict['url'] = url
    json_dict['due'] = due
    json_dict['offered'] = offered
    json_dict['available'] = stat

    json_list.append(json_dict)

with open('programs.json', 'w', encoding='utf-8') as jsonfile:
    json.dump(json_list, jsonfile, indent=4, ensure_ascii=False)
