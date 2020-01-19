from bs4 import BeautifulSoup as bs
from selenium import webdriver
import sys
import io
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import os

path = os.getcwd()
print(path)

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

me = ""
you = ""
msg = MIMEMultipart()

options = webdriver.ChromeOptions()
options.add_argument('disable-gpu')
options.add_argument('headless')


def start_crawling(name_list):
    path = "D:/sportToTo/chromedriver.exe"
    page = webdriver.Chrome(path, chrome_options=options)
    page.get('https://gall.dcinside.com/board/lists?id=lotto')
    page = page.page_source
    soup = bs(page, "lxml")
    file_list = []

    for post in soup.find_all('tr', class_='ub-content us-post'):
        writer = post.find('td', class_='gall_writer ub-writer')
        writer = writer.find('em').text
        for name in name_list:
            if writer == name:
                try:
                    with open('D:/sportToTo/toto_post_number.txt', 'r') as f:
                        post_list = f.read()
                    post_num = post.find('td', class_="gall_num")
                    if post_num.text in post_list:
                        pass
                    else:
                        with open('D:/sportToTo/toto_post_number.txt', 'a') as f:
                            f.write(post_num.text + '\n')
                        page2 = webdriver.Chrome(path, chrome_options=options)
                        page2.set_window_size(1920, 6000)
                        post_url = post.find('td', class_="gall_tit ub-word").a["href"]
                        page2.get("https://gall.dcinside.com" + post_url)
                        image = page2.find_element_by_xpath('//div[@class="view_content_wrap"]')
                        route = 'D:/sportToTo/post' + post_num.text + '.png'
                        file_list.append(route)
                        image.screenshot(route)
                        try:
                            file = open(route, 'rb')
                            img = MIMEImage(file.read())
                            file.close()
                            img.add_header('Content-Disposition', 'attachment', filename=route)
                            msg.attach(img)
                        except Exception as e:
                            print(e)
                except Exception as e:
                    print(e)

    for file in file_list:
        os.remove(file)

    if file_list != []:
        msg['Subject'] = "ToTo Crawling Done"
        msg['From'] = me
        msg['To'] = you
        naver_srv = smtplib.SMTP_SSL("smtp.naver.com", 465)
        naver_srv.login("", "")
        naver_srv.sendmail(from_addr=me, to_addrs=you, msg=msg.as_string())
        naver_srv.quit()


if __name__ == '__main__':
    while True:
        with open('D:/sportToTo/toto_list.txt', encoding='utf-8') as f:
            name_list = [x.strip() for x in f.readlines()]
        start_crawling(name_list)
