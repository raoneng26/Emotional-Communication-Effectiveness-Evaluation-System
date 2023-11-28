import re
import time
import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import paddlehub as hub
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import streamlit as st
from datetime import datetime
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
# import Mytest5_all_get
from datetime import datetime

def convert_date(date_str):
    # 获取当前年份
    current_year = datetime.now().year

    # 尝试不同的日期格式
    for fmt in ["%b %d", "%b %d, %Y"]:
        try:
            dt = datetime.strptime(date_str, fmt)
            # 如果年份是1900（即，输入的日期字符串没有包含年份），则将其设置为当前年份
            if dt.year == 1900:
                dt = dt.replace(year=current_year)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            pass

    # 如果所有格式都无法解析日期，返回None
    return None

lda_news = hub.Module(name="lda_news")

def gmt_trans(dd):
    GMT_FORMAT = '%a %b %d %H:%M:%S +0800 %Y'
    time1 = datetime.strptime(dd, GMT_FORMAT)
    return time1

if True: 
    file2="Twitter japan radioactive.csv"
    cluster = pd.read_csv(file2, encoding='utf-8', sep=';')
    n = 0
    for i in range(0, cluster.shape[1]):
        sheet = cluster.iloc[:, i].values
        if re.match(r"(http|https|ftp)://\S+", str(sheet[0])):
            n = i
            break
        else:
            continue
    sheet = cluster.iloc[:, n].values


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

s = r"D:\电磁辐射网络舆情分析系统\code\chrome-win64\chromedriver.exe"
s = Service(s) #--------------


chrome_options = webdriver.ChromeOptions()
prefs = {'profile.managed_default_content_settings.images': 2}
driver = webdriver.Chrome(service=s)

driver.get('https://twitter.com')
for cookie_name, cookie_value in cookies.items():
    driver.add_cookie({'name': cookie_name, 'value': cookie_value})
url1=r"https://twitter.com/CBKNEWS121/status/1697633057375678612"
driver.get(url1)


driver.implicitly_wait(10)  # 10秒内找到元素就开始执行

class GetTwitterInfo:
    def __init__(self, writer1, publisher1,location1,fan_number1, transmit_count1, comment_count1, like_count1,
                    text2, weibo_tag, id1, sim1):
        self.writer = writer1
        #self.title = title1
        self.publisher = publisher1
        self.transmit_count = transmit_count1
        self.comment_count = comment_count1
        self.like_count = like_count1
        #self.len = length
        #self.play_num = play_number
        self.text = text2
        self.fan_number=fan_number1
        self.loc = location1
        self.wtag = weibo_tag
        self.id = id1
        self.sim = sim1
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
            'Cookie': '_ga=GA1.2.1628544175.1696233997; _gid=GA1.2.1108367702.1696233997; guest_id=v1%3A169640853717306658; kdt=9ak2H4z0b21vo6Al4IOwHmFSMiTwdC7wuBXqUUdN; auth_token=17ea515512edc65153196e4278267832262174c4; ct0=565a96ffd2cf7a4413f54badfe8d98a7c834945a8b4c3db1073d3fec7c755fa1b67f50dbac3d6613f34c9e4aa45bc8691a0a079886314a0abcdb5ed3615b2e1803c91c0abdc228856073e4c5bfe96c16; guest_id_ads=v1%3A169640853717306658; guest_id_marketing=v1%3A169640853717306658; twid=u%3D1709487875321200640; personalization_id="v1_5gT9gfmhsiGmSFXFmGwdNw=="',
            'Connection' : 'close'
        }

      
                 
                
    def get_comment(self):
        # 评论数
        comment_count = self.comment_count
        print(comment_count)

        if comment_count != 0:

            for i in range(1,int(comment_count)+1):
                try:           
                    user_name = driver.find_element(By.XPATH, 
                                                    f"/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/section/div/div/div[{i*2+1}]/div/div/article/div/div/div[2]/div[2]/div[1]/div/div[1]/div/div/div[1]/div/a/div/div[1]/span/span").text
                    print('评论者名称：',user_name)
                    comment =driver.find_element(By.XPATH,
                                                f'/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/section/div/div/div[{i*2+1}]/div/div/article/div/div/div[2]/div[2]/div[2]/div/span').text                       
                    print('评论内容：',comment)     
                    post_time= driver.find_element(By.XPATH,
                                                f'/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/section/div/div/div[{i*2+1}]/div/div/article/div/div/div[2]/div[2]/div[1]/div/div[1]/div/div/div[2]/div/div[3]/a/time').text                       
                    # c_post_time = gmt_trans(post_time)
                    c_post_time=convert_date(post_time)
                    print('评论时间：',c_post_time)    
                    try:
                        like_count=driver.find_element(By.XPATH,
                                                f'/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/section/div/div/div[{i*2+1}]/div/div/article/div/div/div[2]/div[2]/div[3]/div/div/div[3]/div/div/div[2]/span/span/span').text                       
                    except:
                        like_count=0
                    print('点赞数：',like_count)
                    # 定位查看评论者主页，并点击
                    button1 = driver.find_element(By.XPATH, 
                                                    f"/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/section/div/div/div[{i*2+1}]/div/div/article/div/div/div[2]/div[2]/div[1]/div/div[1]/div/div/div[1]/div/a/div/div[1]/span/span")
                    button1.click()  
                    time.sleep(3)     
                    # 粉丝数
                    try:
                        follow_count = driver.find_element(By.XPATH,
                                                    f'/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div[2]/div[5]/div[2]/a/span[1]/span').text 
                        fans = follow_count.replace(',', '') # 移除逗号
                        text1 = ''.join(fans)
                        data = re.findall(r'\d+', text1)
                        data1 = ''.join(data)
                        if data1:  # 检查data1是否为空
                            follow_count = int(float(data1))
                        else:
                            follow_count = 0  # 如果data1为空，设置follow_count为0或其他默认值         
                        print('粉丝数：',follow_count)  
                    except:
                        follow_count = driver.find_element(By.XPATH,
                                                    f'/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[4]/div[2]/a/span[1]/span').text 
                        fans = follow_count.replace(',', '') # 移除逗号
                        text1 = ''.join(fans)
                        data = re.findall(r'\d+', text1)
                        data1 = ''.join(data)
                        if data1:  # 检查data1是否为空
                            follow_count = int(float(data1))
                        else:
                            follow_count = 0  # 如果data1为空，设置follow_count为0或其他默认值         
                        print('粉丝数：',follow_count)  
                    #发布者ip地址
                    try:
                        location = driver.find_element(By.XPATH, 
                                                    "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div/div[4]/div/span[2]/span/span").text
                        # loc = location.split(" ")[1]
                        loc=location
                        print('ip地址：',loc)
                    except:
                        loc=None
                        print('ip地址：',loc)
                    driver.back()  

                    
                except:
                    try:
                        # 定位查看更多按钮，并点击
                        button2 = driver.find_element(By.XPATH, 
                                                        '/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/section/div/div/div[8]/div/div/div/div/div/span')
                        button2.click()         
                        user_name = driver.find_element(By.XPATH, 
                                                        f"/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/section/div/div/div[{i*2+1}]/div/div/article/div/div/div[2]/div[2]/div[1]/div/div[1]/div/div/div[1]/div/a/div/div[1]/span/span").text
                        print('评论者：',user_name)   
                        comment =driver.find_element(By.XPATH,
                                                        f'/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/section/div/div/div[{i*2+1}]/div/div/article/div/div/div[2]/div[2]/div[2]/div/span').text                       
                        print('评论内容：',comment)
                        post_time= driver.find_element(By.XPATH,
                                                    f'/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/section/div/div/div[{i*2+1}]/div/div/article/div/div/div[2]/div[2]/div[1]/div/div[1]/div/div/div[2]/div/div[3]/a/time').text                       
                        c_post_time=convert_date(post_time)
                        print('评论时间：',c_post_time)  
                        try:
                            like_count=driver.find_element(By.XPATH,
                                                f'/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/section/div/div/div[{i*2+1}]/div/div/article/div/div/div[2]/div[2]/div[3]/div/div/div[3]/div/div/div[2]/span/span/span').text                       
                        except:
                            like_count=0
                        print('点赞数：',like_count)
                        # 定位查看评论者主页，并点击
                        button1 = driver.find_element(By.XPATH, 
                                                        f"/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/section/div/div/div[{i*2+1}]/div/div/article/div/div/div[2]/div[2]/div[1]/div/div[1]/div/div/div[1]/div/a/div/div[1]/span/span")
                        button1.click() 
                        time.sleep(3)        
                        
                        try:
                            follow_count = driver.find_element(By.XPATH,
                                                        f'/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div[2]/div[5]/div[2]/a/span[1]/span').text 
                            fans = follow_count.replace(',', '') # 移除逗号
                            text1 = ''.join(fans)
                            data = re.findall(r'\d+', text1)
                            data1 = ''.join(data)
                            if data1:  # 检查data1是否为空
                                follow_count = int(float(data1))
                            else:
                                follow_count = 0  # 如果data1为空，设置follow_count为0或其他默认值         
                            print('粉丝数:',follow_count)  
                        except:
                            follow_count = driver.find_element(By.XPATH,
                                                        f'/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[4]/div[2]/a/span[1]/span').text 
                            fans = follow_count.replace(',', '') # 移除逗号
                            text1 = ''.join(fans)
                            data = re.findall(r'\d+', text1)
                            data1 = ''.join(data)
                            if data1:  # 检查data1是否为空
                                follow_count = int(float(data1))
                            else:
                                follow_count = 0  # 如果data1为空，设置follow_count为0或其他默认值         
                            print('粉丝数:',follow_count)  
                        #发布者ip地址
                        try:
                            location = driver.find_element(By.XPATH, 
                                                        "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div/div[4]/div/span[2]/span/span").text
                            # loc = location.split(" ")[1]
                            loc=location
                            print('ip:',loc)
                        except:
                            loc=None
                            print('ip:',loc)
                        driver.back() 
                    except:
                        continue
                    continue    
        tag=0
        self.writer.writerow(
                        [self.publisher,self.loc,self.fan_number,self.transmit_count, self.comment_count,  self.like_count,
                        self.text, self.wtag, follow_count, user_name,loc,comment, c_post_time, like_count, self.sim, tag])
    def twitter_craw(self):     
        GetTwitterInfo.get_comment(self)
        print('爬虫完成')
                            
def view_bar(num, total):
    rate = float(num) / float(total)
    rate_num = int(rate * 100)
    bar = '\r[%s%s]%d%%,%d' % ("=" * rate_num, "" * (100 - rate_num), rate_num, num)
    sys.stdout.write(bar)
    sys.stdout.flush()           
  
def cleandata(file_name):
    print('---------------------------------------------------------------')
    print("根据主题相似度过滤信息开始")
    data = pd.read_csv(file_name, encoding='utf-8', sep=';')
    sim = data['主题相似度']
    Max = float(max(sim))
    Min = float(min(sim))

    for i in range(0, len(sim)):
        #print(sim[i])
        m = (float(sim[i]) - Min) / (Max - Min)
        #print(m)
        if m <= 0.1:
             # 删除整行数据
            data = data.drop(i, axis=0)  # 注意：drop() 方法不改变原有的 df 数据！
        #sim[i] = m
    # 保存新的csv文件
    data.to_csv("clean-" + file_name, index=False, encoding="utf-8", sep=';')
    print("信息过滤完成,数据保存为：{}".format("clean-" + file_name))

def twitter(writer, url1, num1,key):
    if num1 != 2:
        try:
            driver.get('https://twitter.com')
            for cookie_name, cookie_value in cookies.items():
                driver.add_cookie({'name': cookie_name, 'value': cookie_value})
            driver.get(url1)
            driver.implicitly_wait(10)  # 10秒内找到元素就开始执行 

            # 发布者
            publisher = driver.find_element(By.XPATH,
                                            '/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/section/div/div/div[1]/div/div/article/div/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/div/a/div/div[1]/span/span').text
         
            # 转发数
            transmit = driver.find_element(By.XPATH,
                                           '/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/section/div/div/div[1]/div/div/article/div/div/div[3]/div[5]/div/div/div[2]/div/div/div[2]/span/span/span').text                
            res1 = re.findall(r'\d', transmit)
            transmit_count = ''.join(res1)
            if transmit_count == '':
                transmit_count = 0

            # 评论数
            comment = driver.find_element(By.XPATH,
                                          "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/section/div/div/div[1]/div/div/article/div/div/div[3]/div[5]/div/div/div[1]/div/div/div[2]/span/span/span").text

            res2 = re.findall(r'\d', comment)
            comment_count = ''.join(res2)
            if comment_count == '':
                comment_count = 0

            # 点赞数
            like = driver.find_element(By.XPATH,
                            "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/section/div/div/div[1]/div/div/article/div/div/div[3]/div[5]/div/div/div[3]/div/div/div[2]/span/span/span").text
            res3 = re.findall(r'\d', like)
            like_count = ''.join(res3)
            if like_count == '':
                like_count = 0

            # text
            text2 = driver.find_element(By.XPATH,
                             '/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/section/div/div/div[1]/div/div/article/div/div/div[3]/div[1]/div/div/span[1]').text
            t = re.findall(r'[^\*"/:?\\|<>【】&¥%*@]', text2, re.S)
            t = ''.join(t)

            # tag
            twitter_tag = []
            tags = driver.find_elements(By.XPATH, "//a[starts-with(@href, '/hashtag')]")
            for tag in tags:
                twitter_tag.append(tag.text)
            twitter_tag = ''.join(twitter_tag)

            #帖子账号粉丝数
            url2 = re.sub(r'/status.*', '', url1)
            driver.get(url2)
            fans = driver.find_element(By.XPATH, 
                                    '/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div/div[5]/div[2]/a/span[1]/span').text
            fans = fans.replace(',', '') # 移除逗号
            text1 = ''.join(fans)
            data = re.findall(r'\d+', text1)
            data1 = ''.join(data)
            if data1:  # 检查data1是否为空
                fan_number = int(float(data1))
            else:
                fan_number = 0  # 如果data1为空，设置fan_number为0或其他默认值

            #发布者ip地址
            try:
                location = driver.find_element(By.XPATH, 
                                               "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div/div[4]/div/span[2]/span/span").text
                # loc = location.split(" ")[1]
                loc=location
            except:
                loc=None
            
            driver.back()

            if comment_count != 0:

                #计算主题相似度
                lda_sim = lda_news.cal_query_doc_similarity(query=key, document=t)
                print("主题相似度为：", lda_sim)

                match = re.search(r'/status/(\d+)', url1)
                if match:
                    video_id = match.group(1)
                    # print(video_id) 
                else:
                    video_id="None"
                # getinfo = GetWeiboInfo(writer, title, publisher, transmit_count, comment_count, like_count, length,
                #                        play_number, text2, twitter_tag, video_id)
                   

                getinfo = GetTwitterInfo(writer, publisher,loc,fan_number, transmit_count, comment_count, like_count,
                                         t, twitter_tag, video_id,lda_sim)
                getinfo.twitter_craw()


        except (Exception, BaseException) as e:
            print(e)
            num1 += 1
            twitter(writer, url1, num1,key)
    else:
        return False
    
if True:
    key='japan radioactive'
    file2 = 'Twitter ' + key + '数据.csv'
    with open(file2, "a+", errors="ignore", newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(
            ["发布者","IP属地","帖子账号粉丝数", "转发数", "评论数", "点赞数", "文本", "话题", "一级账号粉丝数","用户名","评论属地", "评论内容", "评论时间", "评论点赞数", "主题相似度" ,"标记"])
        rows = len(sheet)
        for i in range(0, rows):
            url = sheet[i]
            twitter(writer, url, 0,key)
            time.sleep(10)
            view_bar(i, rows)

        # st.success("\n数据爬取结束，原始数据保存为：{}".format(file2))
        data2 = pd.read_csv(file2, encoding='utf-8', sep=';',dtype={'columnname': np.float64})
        # st.write(data2)

        # st.info('根据主题相似度过滤：')
        cleandata(file2)
        # st.info("信息过滤完成,数据保存为：{}".format("clean-" + file2))
        clean_data = pd.read_csv(filepath_or_buffer="clean-" + file2, encoding='utf-8', sep=';')

        # st.write(clean_data)

