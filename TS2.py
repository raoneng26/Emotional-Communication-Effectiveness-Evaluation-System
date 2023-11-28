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
import Mytest5_all_get
# import driver

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

def douyin_slide():
    # temp_height = 1
    for j in range(1, 200):
        driver.execute_script("scrollBy(0,10000)")  # 执行拖动滚动条操作
        # check_height = driver.execute_script(
        #     "return document.documentElement.scrollTop || document.body.scrollTop;")
        time.sleep(2)
        try:
            end = driver.find_element_by_xpath("//div[@class='_5711aa3bb8cc604a63af009da08a1e20-scss']").text
            if "没有" in end:
                break
        except:
            continue

def kuaishou_slide():
    for j in range(1, 200):
        time.sleep(2)
        driver.execute_script("scrollBy(0,10000)")
        try:
            end = driver.find_element_by_xpath("//div[@class='spinning search-loading']").text
            if '已经到底了' in end:
                break
        except:
            continue

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
            ('0','微博', 'Twitter'))

    #爬取微博帖子url
        if website == '微博':
            file = '微博' + keyword + '.csv'
            date = st.text_input('请输入起止时间(eg.2021-09-01-0:2022-03-08-23):')
            if date:
                st.info('请前往微博页面完成登陆')
                weibo_url = 'https://s.weibo.com/'
                # s = Service(r"/usr/local/bin/chromedriver")
                # current_directory = os.getcwd()   #------------
                # s = current_directory+r"\code\chromedriver.exe"
                s = r"D:\电磁辐射网络舆情分析系统\code\chrome-win64\chromedriver.exe"
                s = Service(s) #--------------
                driver = webdriver.Chrome(service=s)
                driver.get(weibo_url)
                time.sleep(30)

                with open(file, "a+", errors="ignore", newline='', encoding='utf-8') as fp:
                    titles = ["发布者", "发布时间", "博客url链接"]
                    writer = csv.DictWriter(fp, fieldnames=titles, delimiter=';')
                    writer.writeheader()
                    for i in range(1, 50):
                        try:
                            w_url = f"https://s.weibo.com/weibo?q={keyword}&timescope=custom:{date}&Refer=g&sudaref=s.weibo.com&page={i}"
                            # w_url = f"https://s.weibo.com/weibo?q={self.keyword}&typeall=1&hasvideo=1&timescope=custom:{date}&Refer=g&page={i}"
                            driver.get(w_url)
                            driver.implicitly_wait(10)
                            blogs = driver.find_elements(By.XPATH, "//div[@class='main-full']//div[@class='card-wrap']")
                            if blogs:
                                for blog in blogs:

                                    publish_time = blog.find_element(By.CSS_SELECTOR,
                                                                    "div.from> a:nth-child(1)").text
                                    up_name = blog.find_element(By.CSS_SELECTOR, ".name").text
                                    try:
                                        blog_url = blog.find_element(By.CSS_SELECTOR,
                                                                    "div.from> a:nth-child(1)").get_attribute('href')
                                    except:
                                        blog_url = 'NULL'
                                    writer.writerow({"发布者": up_name, "发布时间": publish_time, "博客url链接": blog_url})

                            else:
                                st.warning('爬取失败')
                        except:
                            st.warning('一共爬取了'+str(i-1)+'页,'+'页数' + str(i) + '不存在')
                            break

                driver.close()
                st.success('爬取结束，数据保存为：{}'.format(file))

                data1 = pd.read_csv(file, encoding='utf-8', sep=';',engine = "python")
                st.write(data1)

    #爬取Twitter帖子url
        if website == 'Twitter':
            file = 'Twitter ' + keyword + '.csv'
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

 

                # driver.close()
                # st.success('爬取结束，数据保存为：{}'.format(file))

                # data5 = pd.read_csv(file, encoding='utf-8', sep=';', engine="python")
                # st.write(data5)

 


    # ========================================================================================
    if side_bar == '爬取数据':
        initial()

        st.title('爬取数据')
        key = st.text_input('请输入爬取的关键词:')
        file2 = st.file_uploader("请上传爬取的url文件：")
        if file2 is not None:
            st.success('upload success!')
        else:
            st.error('upload failed!')

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

        web = website = st.selectbox(
            '请选择要爬取的网站:',
            ('0','微博', 'Twitter'))



        if website == '微博':

            file1 = '微博' + key + '数据.csv'
            with open(file1, "a+", errors="ignore", newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerow(
                    ["发布者","IP属地","帖子账号粉丝数", "转发数", "评论数", "点赞数", "文本", "话题", "一级账号粉丝数","用户名","评论属地", "评论内容", "评论时间", "评论点赞数", "主题相似度" ,"标记"])
                rows = len(sheet)
                for i in range(0, rows):
                    url = sheet[i]
                    all_get.weibo(writer, url, 0,key)
                    time.sleep(10)
                    all_get.view_bar(i, rows)

                st.success("\n数据爬取结束，原始数据保存为：{}".format(file1))
                data2 = pd.read_csv(file1, encoding='utf-8', sep=';',dtype={'columnname': np.float64})
                st.write(data2)

                st.info('根据主题相似度过滤：')
                all_get.cleandata(file1)
                st.info("信息过滤完成,数据保存为：{}".format("clean-" + file1))
                clean_data = pd.read_csv(filepath_or_buffer="clean-" + file1, encoding='utf-8', sep=';')

                st.write(clean_data)


        if website == 'Twitter':
            file2 = 'Twitter ' + key + '数据.csv'
            with open(file2, "a+", errors="ignore", newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerow(
                    ["发布者","IP属地","帖子账号粉丝数", "转发数", "评论数", "点赞数", "文本", "话题", "一级账号粉丝数","用户名","评论属地", "评论内容", "评论时间", "评论点赞数", "主题相似度" ,"标记"])
                rows = len(sheet)
                for i in range(0, rows):
                    url = sheet[i]
                    Mytest5_all_get.twitter(writer, url, 0,key)
                    time.sleep(10)
                    Mytest5_all_get.view_bar(i, rows)

                st.success("\n数据爬取结束，原始数据保存为：{}".format(file2))
                data2 = pd.read_csv(file2, encoding='utf-8', sep=';',dtype={'columnname': np.float64})
                st.write(data2)

                st.info('根据主题相似度过滤：')
                Mytest5_all_get.cleandata(file2)
                st.info("信息过滤完成,数据保存为：{}".format("clean-" + file2))
                clean_data = pd.read_csv(filepath_or_buffer="clean-" + file2, encoding='utf-8', sep=';')

                st.write(clean_data)




    # ========================================================================================
    if side_bar == '群体情绪计算':
        initial()
        st.title('群体情绪计算')
        uploaded_file1 = st.file_uploader("请上传爬取的文件")
        if uploaded_file1 is not None:
            st.success('upload success!')
        else:
            st.error('upload failed!')
        if st.button('开始计算'):
            emotion_analysis(uploaded_file1.name)
            st.write('计算结束')



    # ========================================================================================
    if side_bar == '结果分析':
        initial()
        st.title('结果分析')
        uploaded_file2 = st.file_uploader("请上传爬取的文件(请确保该数据的情绪计算结果保存在同一目录下）")
        if uploaded_file2 is not None:
            st.success('upload success!')
            #bo = st.selectbox('数据情感分析结果：',
                            #('群体情绪排行榜', '群体情绪中国地图', '集群密度排行', '点赞评论转发占比图', '群体情绪趋势图'))
            bo = st.selectbox('数据情感分析结果：',
                            ('群体情绪排行榜', '集群密度排行', '点赞评论转发占比图', '群体情绪趋势图'))
            test.analysis(bo, uploaded_file2)
        else:
            st.error('upload failed!')



if __name__ == '__main__':  # 不用命令端输入“streamlit run app.py”而直接运行
    if runtime.exists():
        main()
    else:
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())





