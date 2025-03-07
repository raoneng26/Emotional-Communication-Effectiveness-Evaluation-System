import streamlit as st
import pandas as pd
from pyecharts.charts import Bar
from pyecharts.charts import Map
from pyecharts.faker import Faker
import streamlit_echarts
from pyecharts import options as opts
from pyecharts.globals import ThemeType
from streamlit_echarts import st_echarts
from streamlit_echarts import st_pyecharts
from streamlit.components.v1 import html
import main
import 画图
import numpy as np
import re


def get_middle_part(file_name):
    file_name = re.sub(r'\s?\([^)]*\)', '', file_name)
    # 去除文件扩展名
    file_name = file_name.split('.')[0]
    # 按照 "-" 分割文件名
    parts = file_name.split('-')
    
    if len(parts) > 1:
        middle_part = parts[1]
    else:
        middle_part = parts[0]
    
    return middle_part


def normalize_location_names(locations):
    provinces = ['河南', '江苏', '山西', '福建', '四川', '海南', '吉林', '安徽', '浙江', '陕西', '黑龙江', '广东',  '河北', '山东', '辽宁', '云南', '湖北', '江西', '湖南', '甘肃', '贵州','青海','台湾']
    municipalities = ['天津', '重庆', '北京', '上海']
    special_administrative_regions = ['香港', '澳门']
    autonomous_regions = {'新疆': '新疆维吾尔自治区','内蒙古': '内蒙古自治区','西藏': '西藏自治区','宁夏': '宁夏回族自治区','广西': '广西壮族自治区'}
    others = ['其他']
    all_locations = provinces + municipalities + list(autonomous_regions.keys()) + special_administrative_regions + others
    new_locations = {}
    for location in locations.keys():
        if location in all_locations:
            if location in provinces:
                new_locations[location + "省"] = locations[location]
            elif location in municipalities:
                new_locations[location + "市"] = locations[location]
            elif location in special_administrative_regions:
                new_locations[location + "特别行政区"] = locations[location]
            elif location in autonomous_regions:
                new_locations[autonomous_regions[location]] = locations[location]
            else:
                new_locations[location] = locations[location]
    return new_locations


# uploaded_file = st.file_uploader("Upload your data here")
# if uploaded_file is not None:
#     st.success('upload success!')
#     main.emotion_analysis(uploaded_file.name)
# else:
#     st.error('upload failed!')
# side_bar = st.sidebar.radio(
#     '数据情感分析结果：',
#     ['群体情绪排行榜', '群体情绪中国地图', '集群密度排行', '点赞评论转发占比图', '群体情绪趋势图']
# )

def find_urls(file_path, title_P, title_N):
    # 读取 CSV 文件
    df = pd.read_csv(file_path, encoding='utf-8')

    # 确保 st.session_state.post_url 字典已初始化
    if 'post_url' not in st.session_state:
        st.session_state.post_url = {}

    # 查找正面情绪文本对应的 URL
    url_P = []
    for title in title_P:
        url = df[df['文本'] == title]['url链接'].values
        if len(url) > 0 and pd.notna(url[0]):
            url_P.append(url[0])
        else:
            url_P.append("#")

    # 查找负面情绪文本对应的 URL
    url_N = []
    for title in title_N:
        url = df[df['文本'] == title]['url链接'].values
        if len(url) > 0 and pd.notna(url[0]):
            url_N.append(url[0])
        else:
            url_N.append("#")

    # 将结果添加到 st.session_state
    st.session_state.url_P = url_P
    st.session_state.url_N = url_N

    # 打印结果以确认
    print("Positive URLs:", st.session_state.url_P)
    print("Negative URLs:", st.session_state.url_N)



def analysis(side_bar,uploaded_file):
    if  '珠海' not in uploaded_file.name:
        st.session_state.average_score= 画图.calculate_score_and_average(uploaded_file.name)

    

    if side_bar == '群体情绪排行榜':
        title_P, emotion_P, title_N, emotion_N = 画图.read_data(uploaded_file.name)
        # 对正面情绪进行排序，按情绪值从大到小排序
        sorted_positives = sorted(zip(emotion_P, title_P), key=lambda x: x[0], reverse=True)
        emotion_P_sorted, title_P_sorted = zip(*sorted_positives)

        # 对负面情绪进行排序，按情绪值从小到大排序
        sorted_negatives = sorted(zip(emotion_N, title_N), key=lambda x: x[0])
        emotion_N_sorted, title_N_sorted = zip(*sorted_negatives)

        # 选择前10个数据
        title_P, emotion_P = title_P_sorted[:10], emotion_P_sorted[:10]
        title_N, emotion_N = title_N_sorted[:10], emotion_N_sorted[:10]

        st.session_state.title_N=title_N
        st.session_state.title_P =title_P

        st.session_state.name=None
        path1=get_middle_part(uploaded_file.name)
        clean_file=path1+"/clean-"+path1+'.csv'
        if '珠海' in uploaded_file.name:
            find_urls(clean_file, title_P, title_N)

        url_wl_P=[
            'https://facebook.com/story.php?story_fbid=pfbid025STRYCt3DqJNKB4SMjoDFQJGzbuWhfLyGDYGL7zcF4t2PLiEU2X4CjS9dVarppyZl&id=100064837862450',
            'https://facebook.com/story.php?story_fbid=pfbid02mQYrx2tGo7CTdrUYpi63Mw4Jumj2zaXBd67a8Pc9zPcCghyBTh27yfKsYwsW1zTMl&id=100064837862450',
            'https://facebook.com/story.php?story_fbid=pfbid02mQYrx2tGo7CTdrUYpi63Mw4Jumj2zaXBd67a8Pc9zPcCghyBTh27yfKsYwsW1zTMl&id=100064837862450',
            'https://facebook.com/story.php?story_fbid=pfbid02mQYrx2tGo7CTdrUYpi63Mw4Jumj2zaXBd67a8Pc9zPcCghyBTh27yfKsYwsW1zTMl&id=100064837862450',
            'https://facebook.com/story.php?story_fbid=pfbid02aGMUtr7odbqiTLgi6UqvLGg4t5VUog1nDky9NQFZxyw1xg1Xo5A1cJwgQsYra7uCl&id=100064837862450',
            'https://facebook.com/story.php?story_fbid=pfbid025STRYCt3DqJNKB4SMjoDFQJGzbuWhfLyGDYGL7zcF4t2PLiEU2X4CjS9dVarppyZl&id=100064837862450',
            'https://facebook.com/story.php?story_fbid=pfbid025STRYCt3DqJNKB4SMjoDFQJGzbuWhfLyGDYGL7zcF4t2PLiEU2X4CjS9dVarppyZl&id=100064837862450',
            'https://facebook.com/story.php?story_fbid=pfbid025STRYCt3DqJNKB4SMjoDFQJGzbuWhfLyGDYGL7zcF4t2PLiEU2X4CjS9dVarppyZl&id=100064837862450',
            'https://facebook.com/story.php?story_fbid=pfbid02aGMUtr7odbqiTLgi6UqvLGg4t5VUog1nDky9NQFZxyw1xg1Xo5A1cJwgQsYra7uCl&id=100064837862450',
            'https://facebook.com/story.php?story_fbid=pfbid02aGMUtr7odbqiTLgi6UqvLGg4t5VUog1nDky9NQFZxyw1xg1Xo5A1cJwgQsYra7uCl&id=100064837862450',
        ]
        # url_wl_P.reverse()

        url_sy_P=[
            'https://www.xiaohongshu.com/explore/67332b56000000003c017a65?xsec_token=AB8Awd1Iww05bMbIIYTd8Qt4jBzUP3lUbAeSomitF39e8=&xsec_source=pc_search',
            'https://www.bilibili.com/video/av113469630190074/',
            'https://www.bilibili.com/video/av113478656397749/',
            'https://www.kuaishou.com/short-video/3xyb5dkwvv3hmi2',
            'https://www.bilibili.com/video/av113480753482575/',
            'https://www.douyin.com/video/7437100977301261608',
            'https://www.kuaishou.com/short-video/3xyrmj8g3eyigj2',
            'https://www.douyin.com/video/7437103570962386212',
            'https://www.bilibili.com/video/av113472968920192/',
            'https://www.kuaishou.com/short-video/3x7whruh274sd7u',
        ]
        # url_sy_P.reverse()
               
        url_zh_P=[
            'https://weibo.com/2311965983/P006gBJME?refer_flag=1001030103_',
            'https://weibo.com/5173239667/P04eP4Q4q',
            'https://weibo.com/6901760711/P03g00GSv?refer_flag=1001030103_',
            'https://weibo.com/6017039240/P04cuhiBd?refer_flag=1001030103_',
            'https://weibo.com/7455088119/P00xT1H7d?refer_flag=1001030103_',
            'https://weibo.com/5634865334/OFWRGeyMJ?refer_flag=1001030103_',
            'https://weibo.com/2169306777/OFXeBCVzI?refer_flag=1001030103_',
            'https://weibo.com/1887826062/P000l0gnb?refer_flag=1001030103_',
            'https://weibo.com/1589147860/OFWQGvbHZ?refer_flag=1001030103_',
            'https://weibo.com/5160314833/OFWPTs7gS?refer_flag=1001030103_',
        ]
        # url_zh_P.reverse()

        url_tb_P=[
            'https://tieba.baidu.com/p/9268779635?pid=151226288427&cid=0#151226288427',
            'https://tieba.baidu.com/p/9268779635?pid=151226288427&cid=0#151226288427',
            'https://tieba.baidu.com/p/9265936538?pid=151217870936&cid=0#151217870936',
            'https://tieba.baidu.com/p/9268779635?pid=151226288427&cid=0#151226288427',
        ]
        # url_tb_P.reverse()

        url_hfs_P=[
            'https://weibo.com/7715598783/NibhU6Jrn?refer_flag=1001030103_',
            'https://weibo.com/5336709153/Niyr1rrbP?refer_flag=1001030103_',
            'https://weibo.com/1881576793/Nj49Rs3zf?refer_flag=1001030103_',
            'https://weibo.com/7786519236/NiKpFDiFr?refer_flag=1001030103_',
            'https://weibo.com/3152800551/NiM6twFdM?refer_flag=1001030103_',
            'https://weibo.com/6542878363/NsuBJ91uH?refer_flag=1001030103_',
            'https://weibo.com/6070572279/Ni08mgbQB?refer_flag=1001030103_',
            'https://weibo.com/1647486362/NiLU9FMq8?refer_flag=1001030103_',
            'https://weibo.com/3865996388/Niy1Bh7YQ?refer_flag=1001030103_',
            'https://weibo.com/6436464948/NiaTDpEx8?refer_flag=1001030103_',

        ]
        # url_hfs_P.reverse()

        url_yq_P=[
            'https://weibo.com/1989660417/NooQ57FCM?refer_flag=1001030103_',
            'https://weibo.com/6479869715/NmOFvuwoI?refer_flag=1001030103_',
            'https://weibo.com/7229616073/NlFmR9VzY?refer_flag=1001030103_',
            'https://weibo.com/2964915214/NiGDe9Tmt?refer_flag=1001030103_',
            'https://weibo.com/5513176368/NpEdDlbRg?refer_flag=1001030103_',
            'https://weibo.com/5828047833/NoQSFyEES?refer_flag=1001030103_',
            'https://weibo.com/6872083426/NmLhp0fmR?refer_flag=1001030103_',
            'https://weibo.com/7751868307/Np9NTB4yU?refer_flag=1001030103_',
            'https://weibo.com/1163218074/NmIPacEzw?refer_flag=1001030103_',
            'https://weibo.com/6859841043/NqhiNbJCi?refer_flag=1001030103_',
        ]
        # url_yq_P.reverse()
        
        url_fdc_P=[
            'https://weibo.com/6715525032/NhqJ5DiNq',
            'https://weibo.com/7750822151/O1ukLl3oE',
            'https://weibo.com/2382064902/O6sRF5ebM',
            '#',
            'https://weibo.com/6246658101/Njrzu9IlM',
            'https://weibo.com/2382726881/N4yfjcztI',
            'https://weibo.com/3303480313/NgjM6sfzF',
            'https://weibo.com/2377587254/MrKjwb0gW',
            '#',
            'https://weibo.com/1908194624/N7Xy9mESy',
        ]
        # url_yq_P.reverse()
        
        url_hfs_N=[
            'https://weibo.com/3313907053/NiLdBcSji?refer_flag=1001030103_',
            'https://weibo.com/1896892115/NjiUOciIq?refer_flag=1001030103_',
            'https://weibo.com/1887344341/Ni9rEABMi?refer_flag=1001030103_',
            'https://weibo.com/7010131150/NiZVZ6k50?refer_flag=1001030103_',
            'https://weibo.com/2283354943/NiyPM0mXu?refer_flag=1001030103_',
            'https://weibo.com/2001530981/NjevDwpEO?refer_flag=1001030103_',
            'https://weibo.com/7519935397/Nj4bQzG7h?refer_flag=1001030103_',
            'https://weibo.com/2028810631/NjqDEgmzT?refer_flag=1001030103_',
            'https://weibo.com/2400966427/NivZpfVMx?refer_flag=1001030103_',
            'https://weibo.com/3212714910/Nin0WsOnF?refer_flag=1001030103_',
            
        ]

        url_wl_N=[
            'https://facebook.com/story.php?story_fbid=pfbid0HjFrM1YfjkoCuJosRnvaFwdjewhhuhZWc7rAeepVSnoXX5r8cjjSNfLWesCaXnq9l&id=100047112765345',
            'https://facebook.com/story.php?story_fbid=pfbid02GorNggaiLHTHQxmcgU75btcqA9ScYU1XTQwkAnwDTywL9RT2s7SAbwREYQ5SxSRgl&id=100059422245844',
            'https://facebook.com/story.php?story_fbid=pfbid024orc55f1qK4po9PY2FYNuwYqi5g43HvemV5DGEQsZUFoo8b34n1kAxwonA8bo13kl&id=100064391875569',
            'https://facebook.com/story.php?story_fbid=pfbid024orc55f1qK4po9PY2FYNuwYqi5g43HvemV5DGEQsZUFoo8b34n1kAxwonA8bo13kl&id=100064391875569',
            'https://facebook.com/story.php?story_fbid=pfbid0HDYxDtFyDswmUatSR1NyVRaEvyyWwBYFifWhhvMZfLZTmhzwsJWMnSoKqWB4fSiKl&id=100059551808655',
            'https://facebook.com/story.php?story_fbid=pfbid03vKo5si5TeykWmq3gS9C53ssSHjAFZ2AmgKiZdt6ejaMkQV73EJmU4wAVAPZodJYl&id=100059422245844',
            'https://facebook.com/story.php?story_fbid=pfbid0PYApJEuPkoWKwqbCDjwqN1Ur8h2Un4WThityEbPWtBrDq4eg6oVWXf2iERGERYztl&id=100059422245844',
            'https://facebook.com/story.php?story_fbid=pfbid037WNKpkKWyhgJEpnSjeZ7E7LJkcHozFhyRxJ2ubVWgHv8UdFTJYKCvieJbLmepAeYl&id=100063679001455',
            'https://facebook.com/story.php?story_fbid=pfbid0MEBdpoET2uYqxR1fLdB3k9do35vYXPPxkHW6t3UiNtCNGrKZY9PnmWJujfxMeg3gl&id=100059479812265',
            'https://facebook.com/story.php?story_fbid=pfbid08hVxeFE5fQZaQ5R2r4TBM3HyFLbzCMyduJ9sEQiCtdCudygDpykzpAsfzAZJVFHdl&id=100059456532991', 
        ]

        url_yq_N=[
            'https://weibo.com/5255798521/NbuDxnOgQ?refer_flag=1001030103_',
            'https://weibo.com/1887344341/NpizquEZz?refer_flag=1001030103_',
            'https://weibo.com/3144569207/NiH6Cl6BX?refer_flag=1001030103_',
            'https://weibo.com/2181597154/Nnx9EyS3H?refer_flag=1001030103_',
            'https://weibo.com/3988108065/NiF0P24Pa?refer_flag=1001030103_',
            'https://weibo.com/1683492243/MDsb5mSqJ?refer_flag=1001030103_',
            'https://weibo.com/1156281873/N1SwxADcl?refer_flag=1001030103_',
            'https://weibo.com/5423950163/NpGvpj6Fk?refer_flag=1001030103_',
            'https://weibo.com/5802446902/NqmO5mNiU?refer_flag=1001030103_',
            'https://weibo.com/7277507691/MFSg2wb8F?refer_flag=1001030103_',
        ]

        url_tb_N=[
            'https://tieba.baidu.com/p/9265852341?pid=151217675823&cid=0#151217675823',
            'https://tieba.baidu.com/p/9266533083?pid=151219520561&cid=0#151219520561',
            'https://tieba.baidu.com/p/9267249804?pid=151221636142&cid=0#151221636142',

        ]
    
        url_st_P=[
            'https://weibo.com/1731060613/LiLyNhgPY?refer_flag=1001030103_',
            'https://weibo.com/7898673356/NCtga2Xnr',
            'https://weibo.com/7833149398/NCt8B0GAJ',
            'https://weibo.com/7465578749/Lmbyj8M3o?refer_flag=1001030103_',
            'https://weibo.com/7833149398/NCtafkuSI',
            'https://weibo.com/6773287499/MyMoN7PdN?refer_flag=1001030103_',
            'https://weibo.com/7833149398/NCtcj0TPI',
            'https://weibo.com/1801274095/LmgAHt3yb?refer_flag=1001030103_',
            'https://weibo.com/7316590223/LmgkSayjA?refer_flag=1001030103_',
            'https://weibo.com/7833149398/NCtdzrSTM',
        ]
        # url_st_P.reverse()

        url_zh_N=[
            'https://weibo.com/7546573234/OFWQMbwA0?refer_flag=1001030103_',
            'https://weibo.com/2400966427/OFXcWuhNy?refer_flag=1001030103_',
            'https://weibo.com/1566165751/OFWRzrOUC?refer_flag=1001030103_',
            'https://weibo.com/2465225522/P065smWWF?refer_flag=1001030103_',
            'https://weibo.com/7640847916/P006zcEQT?refer_flag=1001030103_',
            'https://weibo.com/1863031164/P000a7wEO?refer_flag=1001030103_',
            'https://weibo.com/6320224333/OFWPb18dd?refer_flag=1001030103_',
            'https://weibo.com/7808803139/OFOwP15oD?refer_flag=1001030103_',
            'https://weibo.com/1728885132/P01pBrCnw?refer_flag=1001030103_',
            'https://weibo.com/1218816145/P06v4oJjt?refer_flag=1001030103_',
        ]

        url_sy_N=[
            'https://www.kuaishou.com/short-video/3xh7xiik7tebsuc',
            'https://www.kuaishou.com/short-video/3xgd98pqj4v35f4',
            'https://www.kuaishou.com/short-video/3xf2brbd56t5uw4',
            'https://www.douyin.com/video/7437133107272207642',
            'https://www.kuaishou.com/short-video/3xtrjnztxfu9du4',
            'https://www.kuaishou.com/short-video/3x9uy5kf6t5pw8s',
            'https://www.kuaishou.com/short-video/3x2u2wdbjx9gf46',
            'https://www.bilibili.com/video/av113463707898329/',
            'https://www.bilibili.com/video/av113463707898329/',
            'https://www.kuaishou.com/short-video/3xf2brbd56t5uw4',
        ]
     
        url_st_N=[
            'https://weibo.com/7898673356/NCtfSu40C',
            'https://weibo.com/7898673356/NCtgSckSI',
            'https://weibo.com/2824412120/LmBx1kzj8?refer_flag=1001030103_',
            'https://weibo.com/7898673356/NCti6tL8g',
            'https://weibo.com/7898673356/NCtiA2TyC',
            'https://weibo.com/2540451950/Lmz0psopM?refer_flag=1001030103_',
            'https://weibo.com/7898673356/NCtjaF4BL',
            'https://weibo.com/7898673356/NCtjqDB54','#','#',
        ]
        
        url_fdc_N=[
            'https://weibo.com/1775019491/NrASPozCb',
            'https://weibo.com/6881597902/Mqrdt4wZN',
            'https://weibo.com/1618051664/O2QilsVKj',
            '#',
            'https://weibo.com/7296341422/P44P7qjqT',
            'https://weibo.com/1639498782/N6aqBgNfn',
            '#',
            '#',
            'https://weibo.com/2182779452/NloYBBV8g',
            'https://weibo.com/5802446902/MqqiVyxNl',
        ]
        
        if "疫情"in uploaded_file.name:
            url_P=url_yq_P
            url_N=url_yq_N 

        if "核污水"in uploaded_file.name:
            url_P=url_hfs_P
            url_N=url_hfs_N 
        if "三胎" in uploaded_file.name:
            url_P=url_st_P
            url_N=url_st_N
        if "网络" in uploaded_file.name:
            url_P=url_wl_P
            url_N=url_wl_N
        if "珠海"in uploaded_file.name:
            if "微博" in uploaded_file.name:
                url_P=url_zh_P
                url_N=url_zh_N
            elif "贴吧" in uploaded_file.name:
                url_P=url_tb_P
                url_N=url_tb_N 
            elif "所有" in uploaded_file.name:
                url_P=url_sy_P
                url_N=url_sy_N 
            else:
                url_P=st.session_state.url_P
                url_N=st.session_state.url_N

        if "房地产" in uploaded_file.name:
            url_P=url_fdc_P
            url_N=url_fdc_N
            
        if st.session_state.p2=="正面":
            st.session_state.img=[
                "https://i.imgur.com/yCpdmbe.png",
                'https://i.imgur.com/2s7Sd71.jpg'
            ] 
           
            option = {
                'grid': {'top': 10, 'left': 300, 'right': 10, 'bottom': 50},
                'tooltip': {
                    'show': 'true',
                    'trigger': 'axis',
                    'formatter': f'''<div><img src={st.session_state.img[1]} style='width: 240px; height: 200px;'/></div>'''

                },
                'yAxis': {'triggerEvent': 'true', 'data': title_P, 'inverse': 'true'},
                'xAxis': {},
                'series': [{
                    'name': '群体正向情绪',
                    'type': 'bar',
                    'data': [{'value' : i, "url" : url} for i, url in zip(list(emotion_P), url_P)],
                    'itemStyle': {'normal': {'label': {'show': 'true', 'position': 'right', 'textStyle': {'color': 'black'}}}}
                }]
            }

            events1 = {
                "click": "function(params) { window.open(params.data.url, '_blank'); console.log(params.name); return params.name }",
                "dblclick":"function(params) { return [params.type, params.name, params.value] }"
            }

            value1 = st_echarts(options=option, height='450px', width='650px', events=events1)
            
            if value1:
                st.session_state.name=value1

        if st.session_state.p2=="负面":
            option = {'grid': {'top': 48, 'left': 300, 'right': 15, 'bottom': 50},
                      'tooltip': {'trigger': 'axis', 'confine': 'true'},
                      'yAxis': {'triggerEvent': 'true', 'data': title_N, 'inverse': 'true'},
                      'xAxis': {'inverse': 'true'},
                      'series': [{'name': '群体负向情绪', 'type': 'bar', 
                                  'data': [{'value' : i, "url" : url} for i, url in zip(list(emotion_N), url_N)],
                                'itemStyle': {'normal':{'label': {'show': 'true','position': 'right','textStyle': {'color': 'black'}}}}
                }]
            }
            events2 = {
                "click": "function(params) { window.open(params.data.url, '_blank'); console.log(params.name); return params.name }",
                "dblclick":"function(params) { return [params.type, params.name, params.value] }"
            }

            value2=st_echarts(options=option, height='450px', width='650px',events=events2)
            if value2:
                st.session_state.name=value2



    if side_bar == '群体情绪世界地图':
        dic = 画图.emotion_map(uploaded_file.name,st.session_state.average_score) # 第一次分析地图时使用
        # path1=get_middle_part(uploaded_file.name)
        with open(path1+"/map_result.txt",  encoding='utf-8') as file1: 
            str1 = file1.read()  # 读取文件内容
            dic = eval("{" + str1 + "}")
        # # # 将dic1中的每个值减去0.5
        # dic1 = {k: v - 0.5  for k, v in dic.items()}
        # # 去除dic1中值为-0.5的项
        # dic1 = {k: v for k, v in dic1.items() if v != -0.5}

        c = Map(init_opts=opts.InitOpts(bg_color='#DCDCDC'))
        c.add('群体情绪地图', [list(z) for z in zip(dic.keys(), dic.values())], maptype="world")
        c.set_series_opts(label_opts=opts.LabelOpts(is_show=True))
        c.set_global_opts(title_opts=opts.TitleOpts(title='World'),
                        visualmap_opts=opts.VisualMapOpts(max_=1, min_=-1,
                                                            range_color=['#B40404', '#FFFFFF',
                                                                        '#31B404']))
        text = c.render_embed()
        html(text, height=500, width=800)


    if side_bar == '群体情绪中国地图':
        # dic = 画图.emotion_map(uploaded_file.name,st.session_state.average_score)  # 第一次分析地图时使用
        path1=get_middle_part(uploaded_file.name)
        if '珠海' in uploaded_file.name:
            df = pd.read_csv(path1 + "/map_result.csv", encoding='utf-8')
            # 提取“评论属地”和“总平均值”列
            result = df[['评论属地', '总平均值']]
            # 将结果转换为字典
            dic = dict(zip(result['评论属地'], result['总平均值']))
        else:
            with open(path1+"/map_result.txt",  encoding='utf-8') as file1: 
                str1 = file1.read()  # 读取文件内容
                dic = eval("{" + str1 + "}")
        dic1=normalize_location_names(dic)
        # 将dic1中的每个值减去0.5
        # dic1 = {k: v - 0.5  for k, v in dic1.items()}
        # dic1 = {k: v for k, v in dic1.items() if v != -0.5}



        c = Map(init_opts=opts.InitOpts(bg_color='#DCDCDC'))
        c.add('群体情绪地图', [list(z) for z in zip(dic1.keys(), dic1.values())], maptype="china")
        c.set_series_opts(label_opts=opts.LabelOpts(is_show=True))
        c.set_global_opts(title_opts=opts.TitleOpts(title='中国'),
                        visualmap_opts=opts.VisualMapOpts(max_=1, min_=-1,
                                                            range_color=['#B40404', '#FFFFFF',
                                                                        '#31B404']))
        text = c.render_embed()
        # html(text, height=600, width=640)
        html(text, height=500, width=800)


    if side_bar=="群体情绪强度饼图":
        # dic = 画图.emotion_map(uploaded_file.name) # 第一次分析地图时使用
        path1=get_middle_part(uploaded_file.name)
        if '珠海' in uploaded_file.name:      
            df = pd.read_csv(path1 + "/map_result.csv", encoding='utf-8')
            # 提取“评论属地”和“总平均值”列
            result = df[['评论属地', '总平均值']]
            # 将结果转换为字典
            dic = dict(zip(result['评论属地'], result['总平均值']))
        else:      
            with open(path1+"/map_result.txt",  encoding='utf-8') as file1: 
                str1 = file1.read()  # 读取文件内容
                dic = eval("{" + str1 + "}")
              

        dic1=normalize_location_names(dic)
        # 将dic1中的每个值减去0.5
        # dic1 = {k: v - 0.5  for k, v in dic1.items()}
        # dic1 = {k: v for k, v in dic1.items() if v != -0.5}

        dic1_non_zero = {}
        for k, v in dic1.items():
            if v != 0:
                dic1_non_zero[k] = v
        dic1_positive = {}
        dic1_negative = {}
        for k, v in dic1_non_zero.items():
            if v >= 0:
                dic1_positive[k] = v
            else:
                dic1_negative[k] = v
        if st.session_state.p=="正面":
            options_p = {
                "title": {"text": "各地区正面情绪强度饼图", "subtext": "未显示情绪值为零的地区", "left": "center"},
                "tooltip": {"trigger": "item"},
                "legend": {"orient": "vertical", "left": "left",},
                "series": [
                    {
                        "name": "地区",
                        "type": "pie",
                        "radius": "50%",
                        "data": [{"value": v, "name": k} for k, v in dic1_positive.items()],
                        "emphasis": {
                            "itemStyle": {
                                "shadowBlur": 10,
                                "shadowOffsetX": 0,
                                "shadowColor": "rgba(0, 0, 0, 0.5)",
                            }
                        },
                    }
                ],
            }            
            st_echarts(
                    options=options_p, height="600px",)
        if st.session_state.p=="负面":
            options_n = {
                "title": {"text": "各地区负面情绪强度饼图", "subtext": "未显示情绪值为零的地区", "left": "center"},
                "tooltip": {"trigger": "item"},
                "legend": {"orient": "vertical", "left": "left",},
                "series": [
                    {
                        "name": "地区",
                        "type": "pie",
                        "radius": "50%",
                        "data": [{"value": v, "name": k} for k, v in dic1_negative.items()],
                        "emphasis": {
                            "itemStyle": {
                                "shadowBlur": 10,
                                "shadowOffsetX": 0,
                                "shadowColor": "rgba(0, 0, 0, 0.5)",
                            }
                        },
                    }
                ],
            }
            st_echarts(
                    options=options_n, height="600px",)


    if side_bar == '集群密度排行':
        title_D, density = 画图.cluster_density(uploaded_file.name)
        c1, c2 = st.columns([1, 0.3])
        with c1:
            st.write('集群密度排行榜')
        with c2:
            st.empty()
        option = {'grid': {'top': 48, 'left': 300, 'right': 10, 'bottom': 50},
                  'tooltip': {'trigger': 'axis', 'confine': 'true'},
                  'yAxis': {'triggerEvent': 'true', 'data': title_D,
                            'axisLabel': {'show': 'true'}},
                  'xAxis': {},
                  'series': [{'name': '集群密度', 'type': 'bar', 'data': density,
                              'itemStyle': {'normal': {'label': {'show': 'true', 'position': 'right',
                                                                 'textStyle': {'color': 'black'}}}}}]}

        st_echarts(options=option, height='700px', width='700px')
        with st.expander('展开显示全部标题'):
            ld = len(title_D)
            for i in range(0, ld):
                st.write(str(i) + ': ' + title_D[ld - i - 1])
                

    if side_bar == '点赞评论转发占比图':
        p_p, p_n = 画图.emotion_pie(uploaded_file.name,st.session_state.average_score)
        b1, b2, b3 = st.columns([1, 0.3, 0.3])
        with b1:
            st.empty()
        with b2:
            pp = st.button('正面')
        with b3:
            pn = st.button('负面')
        if pp:
            option1 = {'title': {'text': '正面情绪点赞评论转发占比图', 'x': 'center'},
                       'tooltip': {'trigger': 'item', 'formatter': "{a} <br/>{b} : {c} ({d}%)"},
                       'legend': {'orient': 'vertical', 'left': 'left', 'data': ['评论', '转发', '点赞']},
                       'series': [{'name': '访问来源', 'type': 'pie', 'radius': '55%',
                                   'label': {'show': 'true', 'formatter': '{b} : {c} ({d}%)'},
                                   'labelLine': {'show': 'true'},
                                   'data': [{'value': int(p_p["评论"]), 'name': '评论'},
                                            {'value': int(p_p["转发"]), 'name': '转发'},
                                            {'value': int(p_p["点赞"]), 'name': '点赞'}]}]}
            st_echarts(options=option1, height='500px')
        if pn:
            option2 = {'title': {'text': '负面情绪点赞评论转发占比图', 'x': 'center'},
                       'tooltip': {'trigger': 'item', 'formatter': "{a} <br/>{b} : {c} ({d}%)"},
                       'legend': {'orient': 'vertical', 'left': 'left', 'data': ['评论', '转发', '点赞']},
                       'series': [{'name': '访问来源', 'type': 'pie', 'radius': '55%',
                                   'label': {'show': 'true', 'formatter': '{b} : {c} ({d}%)'},
                                   'labelLine': {'show': 'true'},
                                   'data': [{'value': int(p_n["评论"]), 'name': '评论'},
                                            {'value': int(p_n["转发"]), 'name': '转发'},
                                            {'value': int(p_n["点赞"]), 'name': '点赞'}]}]}
            st_echarts(options=option2, height='500px')


    if side_bar == '群体情绪趋势图':
        if "珠海" in uploaded_file.name:
            path1 = get_middle_part(uploaded_file.name)
            df = pd.read_csv(path1 + "/data_num.csv", encoding='utf-8')

            # 提取数据
            dp = df[df['情绪类型'] == '正面'].iloc[:, 1:-1].to_dict(orient='records')[0]
            dz = df[df['情绪类型'] == '中性'].iloc[:, 1:-1].to_dict(orient='records')[0]
            dn = df[df['情绪类型'] == '负面'].iloc[:, 1:-1].to_dict(orient='records')[0]

        else:
            dp, dz, dn = 画图.emotion_tendency(uploaded_file.name,st.session_state.average_score)
            # print(dp,dz,dn)

        if st.session_state.post_url is None:
            st.session_state.post_url = {k: "#" for k in dp.keys()}
        if "三胎" in  uploaded_file.name:
            st.session_state.post_url['2022-02-07']=''
            st.session_state.post_url['2022-04-03']='https://weibo.com/5667408729/LmMHGFL5s?refer_flag=1001030103_'
            st.session_state.post_url['2022-04-02']='https://weibo.com/6143949524/LmDdJlwIX?refer_flag=1001030103_'
            st.session_state.post_url['2022-04-01']='https://weibo.com/7640149802/LmtKrDKxY?refer_flag=1001030103_'
            st.session_state.post_url['2022-03-31']='https://weibo.com/5450010616/Lmklh9YKr?refer_flag=1001030103_'
            st.session_state.post_url['2022-03-30']='https://weibo.com/5182206234/LmaX2scuX?refer_flag=1001030103_'
            st.session_state.post_url['2022-03-24']='https://weibo.com/7532428960/LlgqJpfc2?refer_flag=1001030103_'
            st.session_state.post_url['2022-03-20']='https://weibo.com/7544904057/LkEHZldMS?refer_flag=1001030103_'
            st.session_state.post_url['2022-03-09']='https://weibo.com/5369396977/LiYYCkLT3?refer_flag=1001030103_'
            st.session_state.post_url['2022-03-08']='https://weibo.com/6143280254/LiPAOpPoP?refer_flag=1001030103_'
            st.session_state.post_url['2022-03-07']='https://weibo.com/6082210567/LiG9zdD9w?refer_flag=1001030103_'
            st.session_state.post_url['2022-03-06']='https://weibo.com/6342284705/LiwJZonN6?refer_flag=1001030103_'
            st.session_state.post_url['2022-03-05']='https://weibo.com/6035661337/LinicuR2z?refer_flag=1001030103_'
            st.session_state.post_url['2022-03-02']='https://weibo.com/5513200635/LhUN34cbx?refer_flag=1001030103_'
            st.session_state.post_url['2022-03-01']='https://weibo.com/2243012575/LhLzH6MQ1?refer_flag=1001030103_'
            st.session_state.post_url['2022-02-22']='https://weibo.com/6066487475/LgHAGsksT?refer_flag=1001030103_'
            st.session_state.post_url['2022-02-21']='https://weibo.com/3926910490/Lgy56ykmQ?refer_flag=1001030103_'
            st.session_state.post_url['2022-02-17']='https://weibo.com/1785732764/LfWq3e9Ha?refer_flag=1001030103_'
            st.session_state.post_url['2022-02-09']='https://weibo.com/1895323925/LeJ0sBLvK?refer_flag=1001030103_'
            st.session_state.post_url['2022-02-08']='https://weibo.com/6449317967/LezBA2TFu?refer_flag=1001030103_'
            st.session_state.post_url['2022-02-07']='https://weibo.com/1967280501/Leqco7yvu?refer_flag=1001030103_'
        if "网络" in  uploaded_file.name:
            st.session_state.post_url['2024-05-23']='https://facebook.com/story.php?story_fbid=pfbid0HjFrM1YfjkoCuJosRnvaFwdjewhhuhZWc7rAeepVSnoXX5r8cjjSNfLWesCaXnq9l&id=100047112765345'
            st.session_state.post_url['2024-06-15']='https://facebook.com/story.php?story_fbid=pfbid02JE6tAXHXnAL2pvpyRNWXeGjXwHWiiByBRPvbThDr9o1sXkYL31SszaeuxnSbzc8El&id=100092945240607'
            st.session_state.post_url['2024-06-16']='https://facebook.com/story.php?story_fbid=pfbid02K4NbN6sv7ovtB9XsBdxbqU9WGLgKLqgucvCdgx1eAztk5JNeXyc5AEjSseyvnqqol&id=100000682863575'
            st.session_state.post_url['2024-06-18']='https://facebook.com/story.php?story_fbid=pfbid029B8T2JGu7DAfqsN8oK2AnM3YDGXWem2Jx3QYmuKuBNarM9HTZqcWtAAKSptt6J6tl&id=100044582072702'
            st.session_state.post_url['2024-06-19']='https://facebook.com/story.php?story_fbid=pfbid02vzYCopEu87kj6hFomfWNCyxZvGRFKD42weJuWjWfqLQ9R1WD8yxaepkbMRmjhTucl&id=100053584873398'
        if "珠海" and "微博" in  uploaded_file.name:
            st.session_state.post_url['2024-11-11']='https://weibo.com/2028810631/OFO1hcC83?refer_flag=1001030103_'
            st.session_state.post_url['2024-11-12']='https://weibo.com/1662214194/OFXb1CwAV?refer_flag=1001030103_'
            st.session_state.post_url['2024-11-13']='https://weibo.com/2889942201/P06zsuffP?refer_flag=1001030103_'
            st.session_state.post_url['2024-11-14']='https://weibo.com/1823630913/P0dCipb1Q?refer_flag=1001030103_'
            st.session_state.post_url['2024-11-15']='https://weibo.com/7295655721/P0q0jfVQb?refer_flag=1001030103_'
            
        if "珠海" and "所有" in  uploaded_file.name:
            st.session_state.post_url['2024-11-11']='https://www.bilibili.com/video/av113464647420177/'
            st.session_state.post_url['2024-11-12']='https://www.douyin.com/video/7436351094868970788'
            st.session_state.post_url['2024-11-13']='https://www.douyin.com/video/7436650235683753253'
            st.session_state.post_url['2024-11-14']='https://www.bilibili.com/video/av113478656397749/'
            st.session_state.post_url['2024-11-15']='https://www.bilibili.com/video/av113486558467248/'
            
        if "房地产" in  uploaded_file.name:
            st.session_state.post_url['2023-01-01']='https://weibo.com/1779837945/MmjdLuMv2'
            st.session_state.post_url['2023-01-02']='https://weibo.com/1779837945/MmjdLuMv2'
            st.session_state.post_url['2023-01-03']='https://weibo.com/1779837945/MmjdLuMv2'
            st.session_state.post_url['2023-01-04']='https://weibo.com/1779837945/MmjdLuMv2'
            st.session_state.post_url['2023-01-05']='https://weibo.com/1779837945/MmjdLuMv2'
            st.session_state.post_url['2023-01-06']='https://weibo.com/1779837945/MmjdLuMv2'
            st.session_state.post_url['2023-01-07']='https://weibo.com/1779837945/MmjdLuMv2'
            st.session_state.post_url['2023-01-08']='https://weibo.com/1779837945/MmjdLuMv2'
            st.session_state.post_url['2023-01-09']='https://weibo.com/1779837945/MmjdLuMv2'
            st.session_state.post_url['2023-01-10']='https://weibo.com/1779837945/MmjdLuMv2'
            
        # colors = ['green' if v > 0 else 'yellow' if v == 0 else 'red' for v in list(dp.values())]
        imageUrls = [
                "data_weibo\日本核污水排放\img\1.png",
                "data_weibo\日本核污水排放\img\1.png",
                "data_weibo\日本核污水排放\img\1.png"
            ]
        option = {
            'title': {'text': '群体情绪趋势图'},
            'legend': {'data': ['正面', '中性', '负面']},
            'xAxis': {'type': 'category', 'data': [list(z) for z in zip(dp.keys())], 'axisLabel': {'interval': 0}},
            'yAxis': {'type': 'value'},
            'tooltip': {               
                'show': 'true',
                'trigger': 'axis',
                'formatter': '''<div><img src='https://i.imgur.com/ocrN2uf.jpg' style='width: 180px; height: 150px;'/> 
                <br/> <span style='color: #57caf4;'>●</span> 正面: <span style='color: #333; font-weight: bold;'>  {c0}
                </span><br/><span style='color: #76c900;'>●</span> 中性: <span style='color: #333; font-weight: bold;'>  {c1}
                </span><br/><span style='color: #f1c40f;'>●</span> 负面: <span style='color: #333; font-weight: bold;'>  {c2}</span></div>'''
            },
            'dataZoom': {
                'type': 'slider', 
                'xAxisIndex': [0], 
                'show': 'true', 
                'height': 20, 
                'bottom': 0,
                'zoomLock': 'true', 
                'minValueSpan': 0, 
                'maxValueSpan': 7, 
                'realtime': 'true',
                'showDetail': 'false', 
                'filterMode': 'empty'
            },
            # 指定图标的类型
            'series': [
                {'name': '正面', 
                "type": "line", 
                "itemStyle": {
                    "normal": {
                        "label": {
                            "show": True,
                            "position": "top",
                            "formatter": "{c}"
                        }
                    }
                },
                "data": [{'value' : i, "url" : url} for i, url in zip(list(dp.values()), st.session_state.post_url.values())]
                },
                {'name': '中性', 
                "type": "line", 
                "itemStyle": {
                    "normal": {
                        "label": {
                            "show": True,
                            "position": "top",
                            "formatter": "{c}"
                        }
                    }
                },
                "data": [{'value' : i, "url" : url} for i, url in zip(list(dz.values()), st.session_state.post_url.values())]
                },
                {'name': '负面', 
                "type": "line", 
                "itemStyle": {
                    "normal": {
                        "label": {
                            "show": True,
                            "position": "top",
                            "formatter": "{c}"
                        }
                    }
                },
                "data": [{'value' : i, "url" : url} for i, url in zip(list(dn.values()), st.session_state.post_url.values())]
                }
            ]
        }

        events = {
            "click": """function(params) { window.open(params.data.url, '_blank'); }"""
        }

        st.session_state.data = st_echarts(options=option, height='500px', width='1050px', events=events)


    if side_bar == '单视频情绪极性':
            emotion_list = []
            with open(uploaded_file,  'r') as f:  ##更改点
                for line in f.readlines():
                    line = line.strip('\n')
                    emotion_list.append(line)
            print(emotion_list)
            emotion_key = ['生气', '反感', '害怕', '高兴', '悲伤', '惊讶']  # mosei
            emotion_colors = ['#FF7F7F', '#7FFF7F', '#7F7FFF', '#FFFF7F', '#7FFFFF', '#FF7FFF']  # 为每种情绪设置一种颜色
            emotion_data = [{'value': emotion_list[i], 'itemStyle': {'color': emotion_colors[i]}} for i in range(len(emotion_list))]
            # 显示视频情绪极性
            max_emotion = emotion_key[np.argmax(emotion_list)]
            negative = ['生气', '反感', '害怕', '悲伤']
            positive = ['高兴', '惊讶']
            if max_emotion in positive:
                st.success('该视频情绪是积极的')  ##显示语言
            if max_emotion in negative:
                st.error('该视频情绪是消极的')  # 显示语言
            option = {
                'grid': {'top': 10, 'left': 50, 'right': 50, 'bottom': 50},
                'tooltip': {'trigger': 'axis', 'confine': 'true'},
                'yAxis': {'triggerEvent': 'true', 'data': emotion_key},
                'xAxis': {},
                'series': [{
                    'name': 'emotion',
                    'type': 'bar',
                    'data': emotion_data,
                    'itemStyle': {
                        'normal': {
                            'label': {
                                'show': 'true',
                                'position': 'right',
                                'textStyle': {'color': 'black'}
                            }
                        }
                    }
                }]
            }

            st_echarts(options=option, height='400px', width='300px')
    
    
    if side_bar == '单视频模态细粒度':
        data = pd.read_csv(uploaded_file,encoding='utf-8', sep=';') 
        option = {  # 提示框，鼠标悬浮交互时的信息提示
            # 'title': {'text': ' 单模态分析结果'},
            'tooltip': {'show': 'true',  # 是否显示
                        'trigger': 'axis',  # 触发类型，默认数据触发，见下图，可选为：'item' | 'axis'
                        'axisPointer': {
                            'type': 'shadow'
                        }
                        },
            'legend': {},
            'grid': {
                'left': '3%',
                'right': '4%',
                'bottom': '3%',
                'containLabel': 'true'
            },
            'xAxis': {
                'type': 'value'
            },
            'yAxis': {
                'type': 'category',
                'data': [' 文本（负相关）', '视频', '音频']
            },
            'series': [
                {
                    'name': '生气',
                    'type': 'bar',
                    'stack': 'total',
                    'label': {
                        'show': 'true'
                    },
                    'emphasis': {
                        'focus': 'series'
                    },
                    'data': [float(data['angry'][i]) for i in range(3)]
                },
                {
                    'name': '反感',
                    'type': 'bar',
                    'stack': 'total',
                    'label': {
                        'show': 'true'
                    },
                    'emphasis': {
                        'focus': 'series'
                    },
                    'data': [float(data['disgusted'][i]) for i in range(3)]
                },
                {
                    'name': '害怕',
                    'type': 'bar',
                    'stack': 'total',
                    'label': {
                        'show': 'true'
                    },
                    'emphasis': {
                        'focus': 'series'
                    },
                    'data': [float(data['fear'][i]) for i in range(3)]
                },
                {
                    'name': '高兴',
                    'type': 'bar',
                    'stack': 'total',
                    'label': {
                        'show': 'true'
                    },
                    'emphasis': {
                        'focus': 'series'
                    },
                    'data': [float(data['happy'][i]) for i in range(3)]
                },
                {
                    'name': '悲伤',
                    'type': 'bar',
                    'stack': 'total',
                    'label': {
                        'show': 'true'
                    },
                    'emphasis': {
                        'focus': 'series'
                    },
                    'data': [float(data['sad'][i]) for i in range(3)]
                },
                {
                    'name': '惊讶',
                    'type': 'bar',
                    'stack': 'total',
                    'label': {
                        'show': 'true'
                    },
                    'emphasis': {
                        'focus': 'series'
                    },
                    'data': [float(data['surprise'][i]) for i in range(3)]
                }

            ]
        }
        st_echarts(options=option, height='400px')
   
