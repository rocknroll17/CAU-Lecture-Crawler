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
driver.find_element_by_name("password").send_keys("여기에 비밀번호")
driver.find_element_by_name("password").send_keys(Keys.RETURN)
time.sleep(0.5)
'''
driver.get('http://rainbow.cau.ac.kr/site/program/recruit/list?menuid=001004001001&type=C&pagesize=1&currentpage=1')
res = driver.page_source
soup = BeautifulSoup(res,"html.parser")

total = soup.select('#container > p')

total = str(total)
total = int(total[26:31])
print(total)
'''
total = 7000
if total%1500 == 0:
    pages = int(total/1500)
else:
    pages = int(total/1500) +1


status = 0
json_list = []
for j in range(pages):
    driver.get('http://rainbow.cau.ac.kr/site/program/recruit/list?menuid=001004001001&type=C&pagesize=1500&currentpage='+str(j+1))
    res = driver.page_source
    soup = BeautifulSoup(res,"html.parser")
    if j == pages - 1:
        num = total%1500
    else:
        num = 1500
    for i in range(num):
        role_list = []
        form_list = []
        city_list = []
        status += 1
        company = soup.select('#container > div.table_style1 > table > tbody > tr:nth-of-type('+str(1 + i)+') > td:nth-of-type(1)')
        recruit = soup.select('#container > div.table_style1 > table > tbody > tr:nth-of-type('+str(1 + i)+') > td:nth-of-type(2) > a')
        start = soup.select('#container > div.table_style1 > table > tbody > tr:nth-of-type('+str(1 + i)+') > td:nth-of-type(3)')
        finish = soup.select('#container > div.table_style1 > table > tbody > tr:nth-of-type('+str(1 + i)+') > td:nth-of-type(4)')
        role = soup.select('#container > div.table_style1 > table > tbody > tr:nth-of-type('+str(1 + i)+') > td:nth-of-type(5)')
        form = soup.select('#container > div.table_style1 > table > tbody > tr:nth-of-type('+str(1 + i)+') > td:nth-of-type(2) > div > span')
        company = str(company)
        company = company[46:-6]
        if '&amp;' in company:
            company = company.replace('&amp;','&')
        if '&lt;' in company:
            company = company.replace('&lt;','<')
        if '&gt;' in company:
            company = company.replace('&gt;','>')
        if '\xa0' in company:
            company = company.replace('\xa0', ' ')
        recruit = str(recruit)
        recruit = recruit[145:-5]
        if '&amp;' in recruit:
            recruit = recruit.replace('&amp;','&')
        if '&lt;' in recruit:
            recruit = recruit.replace('&lt;','<')
        if '&gt;' in recruit:
            recruit = recruit.replace('&gt;','>')
        if '\xa0' in recruit:
            recruit = recruit.replace('\xa0', ' ')
        start = str(start)
        start = start[5:-6]
        start_year = start[0:4]
        start_month = start[5:7]
        start_date = start[8:10]
        finish = str(finish)
        finish = finish[5:-6]
        finish_year = finish[0:4]
        finish_month = finish[5:7]
        finish_date = finish[8:10]
        role = str(role)
        role = role[5:-6]
        while role[0] == " " or role[0] == '\n':
            role = role[1:]
        while role[-1] == " " or role[-1] == '\n' or role[-1] == '	':
            role = role[:-1]
            
        if '&amp;' in role:
            role = role.replace('&amp;','&')
        if '&lt;' in role:
            role = role.replace('&lt;','<')
        if '&gt;' in role:
            role = role.replace('&gt;','>')
        if '\xa0' in role:
            role = role.replace('\xa0', ' ')
        role_list = (role.split('|'))
        for k in range(len(role_list)):
            while role_list[k][0] == " " or role_list[k][0] == '\n':
                role_list[k] = role_list[k][1:]
            while role_list[k][-1] == " " or role_list[k][-1] == '\n' or role_list[k][-1] == '	':
                role_list[k] = role_list[k][:-1]
        role = role_list[0]
        for k in range(len(role_list) - 1):
            role = role + ', ' + role_list[k + 1]

        form = str(form)
        form = form[87:-8]
        form_list = form.split('<em class="bar2"></em>')
        for k in range(len(form_list)):
            while form_list[k][0] == " " or form_list[k][0] == '\n':
                form_list[k] = form_list[k][1:]
            while form_list[k][-1] == " " or form_list[k][-1] == '\n' or form_list[k][-1] == '	':
                form_list[k] = form_list[k][:-1]
                
        city = form_list[0]
        city_list = city.split(',')
        for k in range(len(city_list)):
            while city_list[k][0] == " " or city_list[k][0] == '\n' or city_list[k][-1] == '	':
                city_list[k] = city_list[k][1:]
            while city_list[k][-1] == " " or city_list[k][-1] == '\n' or city_list[k][-1] == '	':
                city_list[k] = city_list[k][:-1]

        city = city_list[0]
        for k in range(len(city_list) - 1):
            city = city + ', ' + city_list[k + 1]
        
        form_list = form_list[1:]
        form = form_list[0]
        for k in range(len(form_list) - 1):
            form = form + ', ' + form_list[k + 1]
            
        if '&amp;' in form:
            form = form.replace('&amp;','&')
        if '&lt;' in form:
            form = form.replace('&lt;','<')
        if '&gt;' in form:
            form = form.replace('&gt;','>')
        if '\xa0' in form:
            form = form.replace('\xa0', ' ')

        print(status)
        '''
        print(company)
        print(recruit)
        print(start_year)
        print(start_month)
        print(start_date)
        print(finish_year)
        print(finish_month)
        print(finish_date)
        print(role_list)
        '''

        json_dict = {}
        start_dict = {}
        finish_dict = {}
        start_dict['year'] = start_year
        start_dict['month'] = start_month
        start_dict['date'] = start_date
        finish_dict['year'] = finish_year
        finish_dict['month'] = finish_month
        finish_dict['date'] = finish_date
        json_dict['company'] = company
        json_dict['title'] = recruit
        json_dict['from'] = start_dict
        json_dict['to'] = finish_dict
        json_dict['location'] = city
        json_dict['position'] = form
        json_dict['category'] = role
        
        json_list.append(json_dict)

with open('recruit.json', 'w', encoding='utf-8') as jsonfile:
    json.dump(json_list, jsonfile, indent=4, ensure_ascii=False)

driver.quit()
