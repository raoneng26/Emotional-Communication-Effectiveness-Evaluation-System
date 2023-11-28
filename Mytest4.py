import re
import time
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
from bs4 import BeautifulSoup

# lda_news = hub.Module(name="lda_news")
# ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

# def base62_decode(string, alphabet=ALPHABET):
#     """Decode a Base X encoded string into the number

#     Arguments:
#     - `string`: The encoded string
#     - `alphabet`: The alphabet to use for encoding
#     """
#     base = len(alphabet)
#     strlen = len(string)
#     num = 0

#     idx = 0
#     for char in string:
#         power = (strlen - (idx + 1))
#         num += alphabet.index(char) * (base ** power)
#         idx += 1

#     return num

# def url_to_mid(url):
#     '''
#     >>> url_to_mid('z0JH2lOMb')
#     3501756485200075L
#     >>> url_to_mid('z0Ijpwgk7')
#     3501703397689247L
#     >>> url_to_mid('z0IgABdSn')
#     3501701648871479L
#     >>> url_to_mid('z08AUBmUe')
#     3500330408906190L
#     >>> url_to_mid('z06qL6b28')
#     3500247231472384L
#     >>> url_to_mid('yCtxn8IXR')
#     3491700092079471L
#     >>> url_to_mid('yAt1n2xRa')
#     3486913690606804L
#     '''
#     url = str(url)[::-1]
#     size = len(url) // 4 if len(url) % 4 == 0 else len(url) // 4 + 1
#     result = []
#     for i in range(size):
#         s = url[i * 4: (i + 1) * 4][::-1]
#         s = str(base62_decode(str(s)))
#         s_len = len(s)
#         if i < size - 1 and s_len < 7:
#             s = (7 - s_len) * '0' + s
#         result.append(s)
#     result.reverse()
#     return int(''.join(result))

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

    def twitter_craw(writer, url1, num1,key):
        driver.get(url1) 
        driver.implicitly_wait(10)  # 10秒内找到元素就开始执行
        for i in range(10):
        # 评论者
            user_name = driver.find_element(By.XPATH,
                                '/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/section/div/div/div[3]/div/div/article/div/div/div[2]/div[2]/div[1]/div/div[1]/div/div/div[1]/div/a/div/div[1]/span/span').text
                                # /html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/section/div/div/div[4]/div/div/article/div/div/div[2]/div[2]/div[1]/div/div[1]/div/div/div[1]/div/a/div/div[1]/span/span
        
        # comment = comments['data'][i]['text_raw']
        # post_time = comments['data'][i]['created_at']
        # c_post_time = gmt_trans(post_time)
        # like_count = comments['data'][i]['like_counts']
        # follow_count=comments['data'][i]['user']['followers_count']        