import requests
from bs4 import BeautifulSoup as bs
import re
from selenium import webdriver
import sys
import io


sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')


options = webdriver.ChromeOptions()
options.add_argument('disable-gpu')


headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13F69 Safari/601.1', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3,cp949', 'Accept-Encoding': 'none', 'Accept-Language': 'en-US,en;q=0.8', 'Connection': 'keep-alive'}

name_list = ["서울복방에이스", "부산복방에이스", "너굴1", "bee", "부천작동설현", "씨발", "저주인형",
             "방석부 54", "방경섭 70", "정은숙", "ㅇㅇ"]

response = requests.get('https://gall.dcinside.com/board/lists?id=lotto', headers=headers)
response = response.text.split('\'')[1]
# print(response)
response = requests.get(response, headers=headers)
# print(response.text)

path = "D:/sportToTo/chromedriver.exe"
page = webdriver.Chrome(path, chrome_options=options)
page.get("https://gall.dcinside.com/board/lists/?id=loan")
page = page.page_source
soup = bs(page, "lxml")
file_list = []

for post in soup.find_all('tr', class_='ub-content us-post'):
    writer = post.find('td', class_='gall_writer ub-writer')
    writer = writer.find('em').text
    print(writer)
    for name in name_list:
        if writer == name:
            try:
                with open('D:\\sportToTo\\loan_post_number.txt', 'r') as f:
                    post_num = post.find('td', class_="gall_num")
                if post_num.text in f.read():
                    pass
                else:
                    with open('D:\\sportToTo\\loan_post_number.txt', 'a') as f:
                        f.write(post_num + '\n')
                    page2 = webdriver.Chrome(path, chrome_options=options)
                    page2.set_window_size(1920, 6000)
                    post_url = post.find('td', class_="gall_tit ub-word").a
                    print(post_url)
            except Exception as e:
                print(e)
