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


# s = r"D:\电磁辐射网络舆情分析系统\code\chrome-win64\chromedriver.exe"
# s = Service(s) #--------------


# chrome_options = webdriver.ChromeOptions()
# prefs = {'profile.managed_default_content_settings.images': 2}
# driver = webdriver.Chrome(service=s)
# driver.get('https://twitter.com')
# for cookie_name, cookie_value in cookies.items():
#     driver.add_cookie({'name': cookie_name, 'value': cookie_value})
# url1=r"https://twitter.com/AnnalyticTalk/status/1709915125745061949"
# driver.get(url1)


from playwright.sync_api import sync_playwright
from nested_lookup import nested_lookup


def scrape_profile(url: str) -> dict:
    """
    Scrapes Twitter user profile page e.g.:
    https://twitter.com/scrapfly_dev
    returns user data and latest tweets
    """
    _xhr_calls = []

    def intercept_response(response):
        """capture all background requests and save them"""
        # we can extract details from background requests
        if response.request.resource_type == "xhr":
            _xhr_calls.append(response)
        return response

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()
        # enable intercepting for this page

        page.on("response", intercept_response)
        page.goto(url)
        page.wait_for_selector("[data-testid='tweet']")

        user_calls = [f for f in _xhr_calls if "UserBy" in f.url]
        users = {}
        for xhr in user_calls:
            data = xhr.json()
            user_data = data["data"]["user"]["result"]
            users[user_data["legacy"]["screen_name"]] = user_data

        tweet_calls = [f for f in _xhr_calls if "UserTweets" in f.url]
        tweets = []
        for xhr in tweet_calls:
            data = xhr.json()
            xhr_tweets = nested_lookup("tweet_results", data)
            tweets.extend([tweet["result"] for tweet in xhr_tweets])
            users[user_data["legacy"]["screen_name"]] = user_data

    return {"users": users, "tweets": tweets}


if __name__ == "__main__":
    print(scrape_profile("https://twitter.com/Scrapfly_dev"))

