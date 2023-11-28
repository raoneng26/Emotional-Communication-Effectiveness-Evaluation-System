import re
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import paddlehub as hub
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

lda_news = hub.Module(name="lda_news")
ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def base62_decode(string, alphabet=ALPHABET):
    """Decode a Base X encoded string into the number

    Arguments:
    - `string`: The encoded string
    - `alphabet`: The alphabet to use for encoding
    """
    base = len(alphabet)
    strlen = len(string)
    num = 0

    idx = 0
    for char in string:
        power = (strlen - (idx + 1))
        num += alphabet.index(char) * (base ** power)
        idx += 1

    return num

def url_to_mid(url):
    '''
    >>> url_to_mid('z0JH2lOMb')
    3501756485200075L
    >>> url_to_mid('z0Ijpwgk7')
    3501703397689247L
    >>> url_to_mid('z0IgABdSn')
    3501701648871479L
    >>> url_to_mid('z08AUBmUe')
    3500330408906190L
    >>> url_to_mid('z06qL6b28')
    3500247231472384L
    >>> url_to_mid('yCtxn8IXR')
    3491700092079471L
    >>> url_to_mid('yAt1n2xRa')
    3486913690606804L
    '''
    url = str(url)[::-1]
    size = len(url) // 4 if len(url) % 4 == 0 else len(url) // 4 + 1
    result = []
    for i in range(size):
        s = url[i * 4: (i + 1) * 4][::-1]
        s = str(base62_decode(str(s)))
        s_len = len(s)
        if i < size - 1 and s_len < 7:
            s = (7 - s_len) * '0' + s
        result.append(s)
    result.reverse()
    return int(''.join(result))


s = r"D:\电磁辐射网络舆情分析系统\code\chrome-win64\chromedriver.exe"
s = Service(s) #--------------

chrome_options = webdriver.ChromeOptions()
prefs = {'profile.managed_default_content_settings.images': 2}
driver = webdriver.Chrome(service=s)
url1=r"https://weibo.com/5865955200/NhcLNcFqs?refer_flag=1001030103_"
driver.get(url1)
driver.implicitly_wait(10)  # 10秒内找到元素就开始执行
# 视频标题
#title = driver.find_element(By.XPATH, "//div[@class='Detail_tith3_2pyML']").text
#driver.implicitly_wait(10)

# 发布者
publisher = driver.find_element(By.XPATH, "//div[@class='woo-box-flex woo-box-alignCenter head_nick_1yix2']").text

# 博客转发数量
transmit = driver.find_element(By.XPATH,
            "//span[@class='toolbar_num_JXZul']").text

# 博客评论数
comment = driver.find_element(By.XPATH,
            "//div[@class='woo-box-flex woo-box-alignCenter woo-box-justifyCenter toolbar_wrap_np6Ug toolbar_cur_JoD5A']/span[@class='toolbar_num_JXZul']").text

# 博客点赞数量

like = driver.find_element(By.XPATH,
                            "//span[@class='woo-like-count']").text

# text
#text2 = driver.find_element(By.XPATH, "//div[@class='woo-box-item-flex Txt_cut_1Pb86']").text
text2 = driver.find_element(By.XPATH, "//div[@class='detail_wbtext_4CRf9']").text
t = re.findall('[\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\u300b\u4e00-\u9fa5]',
                text2)
#t = re.findall(r'[^\*"/:?\\|<>【】&¥%*@]', t, re.S)
t = ''.join(t)

# tag
weibo_tag = []
#tags = driver.find_elements(By.XPATH, "//div[@class='woo-box-item-flex Txt_cut_1Pb86']//a")
tags = driver.find_elements(By.XPATH, "//div[@class='detail_wbtext_4CRf9']/a")
#//div[@class='detail_wbtext_4CRf9']/a
for tag in tags:
    weibo_tag.append(tag.text)
weibo_tag = ''.join(weibo_tag)



#帖子账号粉丝数
fans = driver.find_element(By.XPATH, "//a[@class='ALink_none_1w6rm PopCard_alink_LHzuI PopCard_pointer_2u0ZP']").text
text1 = ''.join(fans)
if '万' in text1:
    num = re.findall(r'(.+?)万', text1)
    data1 = ''.join(num)
    if '.' in data1:
        number = float(data1) * 10000
    else:
        data1 = re.findall(r'\d+', text1)
        data1 = ''.join(data1)
        number = float(data1) * 10000
    fan_number = int(number)
else:
    data = re.findall(r'\d+', text1)
    data1 = ''.join(data)
    if data1:  # 检查data1是否为空
        fan_number = int(float(data1))
    else:
        fan_number = 0  # 如果data1为空，设置fan_number为0或其他默认值

video_id = driver.find_element(By.XPATH, "//a[@class='head-info_time_6sFQg']").get_attribute('href').split('/')[4]
print(video_id)
video_id = url_to_mid(video_id)


# ip
location = driver.find_element(By.XPATH, "//div[@class='head-info_ip_3ywCW']").text


print(publisher)
print(transmit)
print(comment)
print(like)
print(t)
print(weibo_tag)
# print(video_id)
print(fan_number)
print(video_id)
print(location)