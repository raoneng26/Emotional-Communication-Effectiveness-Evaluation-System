import streamlit as st
import main
import test
import csv
import time
import pandas as pd
import os
import re
import all_get
import numpy as np
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from streamlit import runtime
import sys
from streamlit.web import cli as stcli
from all_get import driver
from main import emotion_analysis

# 账号1
cookies = {
    '_ga': 'GA1.2.1628544175.1696233997',
    '_gid': 'GA1.2.1108367702.1696233997',
    'g_state': '{"i_l":0}',
    'lang': 'en',
    'guest_id': 'v1%3A169640853717306658',
    'kdt': '9ak2H4z0b21vo6Al4IOwHmFSMiTwdC7wuBXqUUdN',
    'auth_token': '17ea515512edc65153196e4278267832262174c4',
    'ct0': '565a96ffd2cf7a4413f54badfe8d98a7c834945a8b4c3db1073d3fec7c755fa1b67f50dbac3d6613f34c9e4aa45bc8691a0a079886314a0abcdb5ed3615b2e1803c91c0abdc228856073e4c5bfe96c16',
    '_twitter_sess': 'BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoHaWQiJTNmMmQ0NjRkMTVjNzNkZjhjMjgyZTY5%250AMTdjOWViNDYwOg9jcmVhdGVkX2F0bCsIs87V%252BYoBOgxjc3JmX2lkIiU0MGYz%250AN2VmMjU3YjBiZGU3NWZlM2QyZjFjZmNmMDJjNg%253D%253D--404064b2053aa8de355b3408ff8ba4e352d914d5',
    'guest_id_ads': 'v1%3A169640853717306658',
    'guest_id_marketing': 'v1%3A169640853717306658',
    'twid': 'u%3D1709487875321200640',
    'personalization_id': '"v1_sTUjp87xxKSdklFNZEa01Q=="'
}

# 账号2
# cookies = {
#     '_ga': 'GA1.2.1628544175.1696233997',
#     '_gid': 'GA1.2.1108367702.1696233997',
#     'guest_id': 'v1%3A169639709088513913',
#     '_twitter_sess': 'BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCHVtJfmKAToMY3NyZl9p%250AZCIlOGY4ODdjOTZlOGJhNDg1MjFiNGJhNmI0NmI1YTY5ZWM6B2lkIiUyYTM2%250ANzZlYWI0NzQwZmY1MjMwYzQ2MzgxYWU4MzhjOA%253D%253D--514c1172f5ab2bbe9355860d17a112fdf4a9a0a9',
#     'kdt': 'upLrSk3khqLOCd1NHezkQILX2n1ut9rdbwRoeHC3',
#     'auth_token': '317e423dfb10ca59584eea5f49f7a4902c4d4264',
#     'ct0': '09382989c8eb20b57e9e86281e7d4ac2c0c737293c15a15ac52a32b5c60d789bcb07a6a40da99fe708a19ecd7e7169cab5e390bd0cad4b871f61a0c9da3f931126707d592a23ac9dcb5b3fa55d3ffef4',
#     'att': '1-qpE1MD79KxKWzcRSi9jKQL9LvbqmBM9kCIGSWWgC',
#     'guest_id_ads': 'v1%3A169639709088513913',
#     'guest_id_marketing': 'v1%3A169639709088513913',
#     'twid': 'u%3D1665693291403411458',
#     'personalization_id': '"v1_a7TKq26czeCKDkBHd4rA5w=="'
# }

def initial():
    global keyword
    keyword = None
    global website
    website = None
    global key
    key = None
    global web
    web = None
    global uploaded_file1
    uploaded_file1 = None
    global uploaded_file2
    uploaded_file2 = None

def main():
    side_bar = st.sidebar.radio(
        '网络舆论分析系统：',
        ['爬取链接', '爬取数据','群体情绪计算', '结果分析']
    )

    # ========================================================================================
    if side_bar == '爬取链接':
        initial()
        st.title('爬取链接')

        keyword = st.text_input('请输入爬取的关键词:')
        website = st.selectbox(
            '请选择要爬取的网站:',
            ('0','Twitter', '哔哩哔哩','抖音'))

    #爬取twitter帖子url
        if website == 'Twitter':
            file = 'Twitter' + keyword + '.csv'
            date = "2021-09-01:2022-03-08"
            date = st.text_input('请输入起止时间(eg.2021-09-01:2022-03-08):')

 
            if date:
                start_date, end_date = date.split(':')  # 将日期范围分割为开始日期和结束日期
                # st.info('请前往微博页面完成登陆')
                weibo_url = 'https://twitter.com/'
                s = r"D:\电磁辐射网络舆情分析系统\code\chrome-win64\chromedriver.exe"
                s = Service(s) #--------------
                driver = webdriver.Chrome(service=s)
                driver.get(weibo_url)
                for cookie_name, cookie_value in cookies.items():
                    driver.add_cookie({'name': cookie_name, 'value': cookie_value})
                time.sleep(10)

                with open(file, "a+", errors="ignore", newline='', encoding='utf-8') as fp:
                    titles = ["发布者", "发布时间", "推文url链接"]
                    writer = csv.DictWriter(fp, fieldnames=titles, delimiter=';')
                    writer.writeheader()
                    for i in range(1, 20):
                        try:
                            w_url=f"https://twitter.com/search?q={keyword}%20until%3A{end_date}%20since%3A{start_date}&src=typed_query"
                            driver.get(w_url)
                            driver.implicitly_wait(10)
                            publish_time = driver.find_element(By.XPATH,
                                                                f"/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/section/div/div/div[{i}]/div/div/article/div/div/div[2]/div[2]/div[1]/div/div[1]/div/div/div[2]/div/div[3]/a/time").text               
                            try:                                        
                                up_name = driver.find_element(By.XPATH,
                                                               f"/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/section/div/div/div[{i}]/div/div/article/div/div/div[2]/div[2]/div[1]/div/div[1]/div/div/div[1]/div/a/div/div[1]/span/span").text
                            except:                                      
                                up_name = driver.find_element(By.XPATH,
                                                               f"/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/section/div/div/div[{i}]/div/div/article/div/div/div[2]/div[2]/div[1]/div[1]/div[1]/div/div/div[1]/div/a/div/div[1]/span/span").text                                                                                                                       
                            try:
                                blog_url = driver.find_element(By.XPATH,
                                                            f"/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/section/div/div/div[{i}]/div/div/article/div/div/div[2]/div[2]/div[1]/div[1]/div[1]/div/div/div[2]/div/div[3]/a").get_attribute('href')
                                # print(blog_url)
                            except:
                                blog_url = 'NULL'
                            writer.writerow({"发布者": up_name, "发布时间": publish_time, "推文url链接": blog_url}) # 保存数据
                            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # 滚动到页面底部
                            time.sleep(1) # 等待新的数据加载
                        except:
                            st.warning('一共爬取了'+str(i-1)+'页,'+'页数' + str(i) + '不存在')
                            break

                driver.close()
                st.success('爬取结束，数据保存为：{}'.format(file))

                data1 = pd.read_csv(file, encoding='utf-8', sep=';',engine = "python")
                st.write(data1)

if __name__ == '__main__':  # 不用命令端输入“streamlit run app.py”而直接运行
    if runtime.exists():
        main()
    else:
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())
