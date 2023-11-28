from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from datetime import datetime
import time
import re

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

s = r"D:\电磁辐射网络舆情分析系统\code\chrome-win64\chromedriver.exe"
s = Service(s) #--------------


chrome_options = webdriver.ChromeOptions()
prefs = {'profile.managed_default_content_settings.images': 2}
driver = webdriver.Chrome(service=s)
driver.get('https://twitter.com')
for cookie_name, cookie_value in cookies.items():
    driver.add_cookie({'name': cookie_name, 'value': cookie_value})
# url1=r"https://twitter.com/CBKNEWS121/status/1697633057375678612"
# driver.get(url1)


target_tweet='https://twitter.com/AnnalyticTalk/status/1709915125745061949'


# Twitter Login 
twitter_usr="@your_twitter_username"
twitter_pass='password'

def twitter_login(driver, twitter_usr=str, twitter_pass=str):
    driver.get('https://twitter.com/i/flow/login')
    time.sleep(6)
    user = driver.find_element(by=By.XPATH, value='//*[@autocomplete="username"]')
    time.sleep(1)
    user.send_keys(twitter_usr)
    time.sleep(1)
    next_btn = driver.find_element(by=By.XPATH, value='/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[6]/div')
    next_btn.click()
    time.sleep(4)
    psswd_in = driver.find_element(by=By.XPATH, value='//*[@autocomplete="current-password"]')
    psswd_in.send_keys(twitter_pass)
    time.sleep(2)
    login_btn = driver.find_element(by=By.XPATH, value='//html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div')
    login_btn.click()
    time.sleep(3)
    print('Login Successful')
    return driver

# driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))

# twitter_login(driver, twitter_usr=twitter_usr, twitter_pass=twitter_pass)

tweets = []

driver.get(target_tweet)

time.sleep(6)

# comment_count = self.comment_count


MAX_SCROLLS=1
for _ in range(MAX_SCROLLS):
    last = driver.find_elements(By.XPATH, '//div[@data-testid="cellInnerDiv"]')[-1]
    driver.execute_script("arguments[0].scrollIntoView(true)", last)
    time.sleep(.2)
    all_tweets = driver.find_elements(By.XPATH, '//div[@data-testid]//article[@data-testid="tweet"]')
    for item in all_tweets[1:]: # skip first tweet because it is BBC tweet
            enter=0 

            try:
                user_name=item.find_element(By.XPATH,'.//a[@role="link"]//div//div[@dir="ltr"]//span//span').text
            except:
                user_name= '[empty]'


            try:
                like = item.find_element(By.XPATH,
                                            './/div/div/div[2]/div[2]/div[3]/div/div/div[3]/div/div/div[2]/span/span/span').text      
                res = re.findall(r'\d', like)
                like_count = ''.join(res)
                if like_count == '':
                    like_count = 0
            except:
                like_count = 0


            try:
                sub_comment_count=item.find_element(By.XPATH,
                                                './/div/div/div[2]/div[2]/div[3]/div/div/div[1]/div/div/div[2]/span/span/span').text
                if sub_comment_count != "0":
                    tag = 1
                else:
                    tag = 0
            except:
                tag = 0


            try:
                date = item.find_element(By.XPATH, './/a[@dir="ltr"]//time').text              
                date=convert_date(date)
              
            except:
                date = '[empty]'

            try:
                text = item.find_element(By.XPATH, './/div[@data-testid="tweetText"]').text
            except:
                text = '[empty]'


            try:
                replying_to = item.find_element(By.XPATH, './/div[contains(text(), "Replying to")]//a').text
            except:
                replying_to = '[empty]'


                
            
            tweets.append([user_name, like_count, date, replying_to, text, tag])
            time.sleep(.2)


            

import pandas as pd

df = pd.DataFrame(tweets, columns=['User Name', 'Like Count', 'Date of Tweet', 'Replying to', 'Tweet', 'Tag'])

print(df)
