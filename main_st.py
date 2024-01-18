from st_on_hover_tabs import on_hover_tabs
from main import emotion_analysis
import streamlit as st
from streamlit import runtime
import sys
from streamlit.web import cli as stcli
import random
import time
import base64
from streamlit.components.v1 import html
import numpy as np
import pandas as pd
from test import analysis
from streamlit_card import card as st_card
from streamlit_elements import elements, mui, html
from streamlit_echarts import st_echarts
import os
from datetime import datetime,timedelta
from docxtpl import DocxTemplate
from docx2pdf import convert
import requests
import re

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


def progress_bar(max_time):
    start_time = time.time()
    progress_placeholder = st.empty()  # 创建一个占位符
    for i in range(1, 101):
        num_progress=i
        progress_placeholder.markdown(f''' 
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Progress_bar</title>
                <link rel="stylesheet" href="progress_bar.css">
            </head>
            <body>
                <div class="container">
                    <section>
                        <article>
                            <!-- <input type="radio" name="switch-color" id="red" checked>
                            <input type="radio" name="switch-color" id="cyan">
                            <input type="radio" name="switch-color" id="lime"> -->
                            <div class="chart">
                                <div class="bar bar-{num_progress} cyan">
                                    <div class="face top">
                                        <div class="growing-bar"><p style="float: right; margin-right:10px"><strong>{num_progress}</strong>%</p></div>
                                    </div>
                                    <div class="face side-0">
                                        <div class="growing-bar"></div>
                                    </div>
                                    <div class="face floor">
                                        <div class="growing-bar"></div>
                                    </div>
                                    <div class="face side-a"></div>
                                    <div class="face side-b"></div>
                                    <div class="face side-1">
                                        <div class="growing-bar"></div>
                                    </div>
                                </div>
                            </div>
                        </article>
                    </section>
                </div> 
            </body>
            </html>''',unsafe_allow_html=True)
        elapsed_time = time.time() - start_time
        if elapsed_time > max_time:
            break
        if i<100:
            sleep_time = random.uniform(0.01, (max_time - elapsed_time) / (100 - i))
            time.sleep(sleep_time)
            progress_placeholder.empty()
    

def get_base64(bin_file): 
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


def set_background(png_file):  # 设置背景图
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/ipg;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)


def upload_file_to_0x0(file_path):
    """上传文件到0x0并返回URL"""
    with open(file_path, 'rb') as f:
        response = requests.post('https://0x0.st', files={'file': f})
    if response.status_code == 200:
        return response.text.strip()
    else:
        return None
    

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


def report_show():
    st.markdown(r'''<style>
                    .box {
                        position: relative;
                    }
                        .box img {
                        width: 300px;
                    }

                    .box .title {
                        position: absolute;
                        left: 15px;
                        bottom: 20px;
                        z-index: 2;
                        width: 260px;
                        color: #fff;
                        font-size: 20px;
                        font-weight: 700;
                    }
                    .box .mask {
                        position: absolute;
                        left: 0;
                        top: 0;

                        opacity: 0;
                        width: 300px;
                        height: 410px;
                        background-image: linear-gradient(
                            transparent,
                            rgba(0,0,0,.6)
                        );
                        transition: all .5s;
                    }
                    .box:hover .mask {
                        opacity: 1;
                    } 
                </style>''',unsafe_allow_html=True)
    reportpath1='report.jpg' # -----------------更改点--------------
    # reporturl=st.session_state.url_pdf
    if "疫情" in st.session_state.file_in.name:
        reporturl=r"https://drive.google.com/file/d/1i8suHggGPvH-QECbR5f9AtrDh9jLULlN/view?usp=sharing"# -----------------更改点--------------

    if "日本" in st.session_state.file_in.name:
        reporturl=r"https://drive.google.com/file/d/1OKFRVaK5IK8Wr9yb368YojmzOh1URxOT/view?usp=sharing"
     
    if "三胎" in st.session_state.file_in.name:
        reporturl=r"https://drive.google.com/file/d/1BVOOybmUD7Dd6hyKJPRTOC2NALh80Qi5/view?usp=sharing"
    with open(reportpath1, "rb") as f:
        data = f.read()
        encoded = base64.b64encode(data)
        data = "data:image/png;base64," + encoded.decode("utf-8")
    st.markdown(f'''
    <body>
        <div class="box">
            <a  href={reporturl}>
            <img src={data} alt="">
            <div class="title">分析报告</div>
            <!-- 渐变背景 -->
            <div class="mask"></div>
            </a>
        </div>
    </body>
    </html>''',unsafe_allow_html=True)


def card_show():
    reportpath='report.jpg'
    bgcpath='bgc.jpg'
    with open(reportpath, "rb") as f:
        data = f.read()
        encoded = base64.b64encode(data)
        data = "data:image/png;base64," + encoded.decode("utf-8")
        # st.markdown(r'''<style>
        #         .css-1mb7ed4 {
        #         background-color: rgba(211, 211, 211, 0.1);
        #         }
                
        #         </style>''',unsafe_allow_html=True)
        
    res = st_card(
    title="分析报告",
    text="analysis",
    image=data,
    styles={
        "card": {
            "width": "250px",
            "height": "320px",
            "border-radius": "60px",
            "box-shadow": "0 0 10px rgba(0,0,0,0.5)",    
        },
    },
    url="https://github.com/gamcoh/st-card",
    on_click=lambda: st.write(''))


def get_middle_part(file_name):
    # 去除文件扩展名
    file_name = file_name.split('.')[0]
    # 按照 "-" 分割文件名
    parts = file_name.split('-')
    
    if len(parts) > 1:
        middle_part = parts[1]
    else:
        middle_part = parts[0]
    
    return middle_part


def change_date(times):
    time2 = []
    for time1 in times:
        time1 = str(time1)[:10]
        time2.append(time1)
    return time2


def find_imppost_data(file_name):
    file_name = re.sub(r'\s?\([^)]*\)', '', file_name)
    path1=get_middle_part(file_name)
    if 'xlsx' in file_name:
        data = pd.read_excel(path1+"/"+file_name)
    else:
        data = pd.read_csv(path1+"/"+file_name, encoding='utf-8', sep=';')
    data['评论时间'] = change_date(data['评论时间'].values)
    df = data.sort_values(by="评论时间", ascending=True)
    df['评论时间'] = pd.to_datetime(df['评论时间'])
    df['日期'] = df['评论时间'].dt.strftime('%Y-%m-%d')
    # print(df['日期'].to_string())
    df_deduplicated = df.drop_duplicates(subset=['发布者', '文本'], keep='first')
    df_sorted = df_deduplicated.sort_values(['日期', '点赞数'], ascending=[True, False])
    posts_dict_poster= pd.Series(df_sorted[[ '发布者']].values.tolist(), index=df_sorted['日期']).to_dict()
    posts_dict = pd.Series(df_sorted[['文本', '发布者']].values.tolist(), index=df_sorted['日期']).to_dict()
    # print(posts_dict)
    return(posts_dict,posts_dict_poster)


def match_url(dict_, csv_file):
    url_data = pd.read_csv(csv_file, encoding='utf-8', sep=';')
    result_dict = {}
    for date, publisher in dict_.items():
        date_str = datetime.strptime(date, '%Y-%m-%d').strftime('%m月%d日')
        matched_row = url_data[(url_data['发布时间'].str.startswith(date_str)) & (url_data['发布者'] == publisher[0])]
        if not matched_row.empty:
            result_dict[date] = matched_row['博客url链接'].values[0]
        else:
            # 如果当天没有找到匹配的数据，尝试在前几天找
            for i in range(1, 8):  # 尝试在前7天找
                prev_date_str = (datetime.strptime(date, '%Y-%m-%d') - timedelta(days=i)).strftime('%m月%d日')
                matched_row_prev = url_data[(url_data['发布时间'].str.startswith(prev_date_str)) & (url_data['发布者'] == publisher[0])]
                if not matched_row_prev.empty:
                    result_dict[date] = matched_row_prev['博客url链接'].values[0]
                    break
            else:
                result_dict[date] = None
    # print(result_dict)
    return result_dict


def main():
    initial()
    st.session_state.style="标准情绪值"

    # st.session_state.file_in=" "
    # st.session_state.file_out=" "
    st.set_page_config(layout="wide")
    set_background("bgc.jpg")  ##更改点（背景图）
    col,col_title,col=st.columns([1.7,4,1])
    with col_title:      
        st.header("热点事件引发的群体情绪传播效果评估系统")
    st.markdown('<style>' + open('./style.css').read() + '</style>', unsafe_allow_html=True)

    # 侧边栏
    with st.sidebar:
        tabs = on_hover_tabs(tabName=['Start', 'Regional Analysis', 'Time Domain', 'Comparative Ranking'], 
                            iconName=['star', 'language', 'schedule', 'leaderboard'], default_choice=0)


    if tabs =='Start': 
        st.session_state.file_in=" "
        st.subheader('数据爬取')
        # with st.expander(" ",True):
        keyword = st.text_input('请输入关键词:')
        st.session_state.keyword =" "
        st.session_state.website =" "
        if keyword:
            st.session_state.keyword =keyword
            website = st.selectbox('请选择爬取网站:',(' ','微博', 'Twitter'))
        else:
            website = " "
        st.session_state.website=website
        if website != ' ':       
            file1 = '微博' + keyword + '数据.csv'
            with open(file1, "a+", errors="ignore", newline='', encoding='utf-8') as f:
                with open('progress_bar.css', 'r',) as f:
                    st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)
                st.markdown(f'''
                <body>
                <div class="container " style="height:200px">
                    <header>
                        <h1 style="height:20px">关键词：<strong>{keyword}</strong></h1>
                        <p style="height:30px">... please wait for a moment ...</p>
                    </header>
                </div>
                </body>''',unsafe_allow_html=True)
                progress_bar(3)
                st.markdown(r'''<style>
                            .success {
                            color: white;
                            background-color: rgba(33, 195, 84, 0.1);
                            border-color: #28a745;
                            padding: 10px;
                            margin: 10px;
                            border-radius: 4px;
                            }
                            
                            </style>''',unsafe_allow_html=True)
                st.markdown(f'''
                    <html>
                        <body>
                            <div class="success "style="height:56px">
                            <p style="height:2em ;margin: 0 auto ; max-width:100%; padding: 0; line-height: 2em; color: rgb(23, 114, 51);">数据爬取并过滤完成，数据信息保存为：{file1}</p>
                            </div>
                        </body>
                    </html>
                ''',unsafe_allow_html=True)
                if '日本'in keyword:
                    file_clean="微博日本核污水排放数据/clean-微博日本核污水排放数据.csv"  # ------------------------更改点------------------------------
                    downloadfile_name="clean-微博日本核污水排放数据.csv"
                    file_path="微博日本核污水排放数据"

                if '疫情'in keyword:
                    file_clean="微博疫情后的经济数据/clean-微博疫情后的经济数据.csv"  # ------------------------更改点------------------------------
                    downloadfile_name="clean-微博疫情后的经济数据.csv"
                    file_path="微博疫情后的经济数据"

                if '三胎'in keyword:
                    file_clean="微博三胎政策数据/clean-微博三胎政策数据.csv"  # ------------------------更改点------------------------------
                    downloadfile_name="clean-微博三胎政策数据.csv"
                    file_path="微博三胎政策数据"   
                    st.session_state.keyword="三胎"             

                # path=file_path
                # # 对字典进行排序
                # with open(path+"/map_result.txt",  encoding='utf-8') as file1: 
                #     str1 = file1.read()  # 读取文件内容
                #     dic = eval("{" + str1 + "}")
                # dic1=normalize_location_names(dic)
                # positive_items = sorted([(k, v) for k, v in dic1.items() if v > 0], key=lambda x: x[1], reverse=True)
                # negative_items = sorted([(k, v) for k, v in dic1.items() if v < 0], key=lambda x: x[1])
                # # 获取前两个最大的正值和负值
                # top_2_positive = positive_items[:2] if positive_items else [("无", "")]
                # top_2_negative = negative_items[:2] if negative_items else [("无", "")]
                # # 格式化为字符串
                # positive_str = ", ".join(["{}({})".format(k, v) for k, v in top_2_positive]) if positive_items else "无"
                # negative_str = ", ".join(["{}({})".format(k, v) for k, v in top_2_negative]) if negative_items else "无"
                # print("正值最大的前两个地点和值：", positive_str)
                # print("负值最大的前两个地点和值：", negative_str)
                # # 读取dp字典
                # with open(path + '/dp_result.txt', 'r', encoding='utf-8') as f:
                #     dp = eval("{" + f.read() + "}")
                # # 读取dz字典
                # with open(path + '/dz_result.txt', 'r', encoding='utf-8') as f:
                #     dz = eval("{" + f.read() + "}")
                # # 读取dn字典
                # with open(path + '/dn_result.txt', 'r', encoding='utf-8') as f:
                #     dn = eval("{" + f.read() + "}")
                # # 找到数量最多的日期和数量
                # max_dp_date, max_dp_count = max(dp.items(), key=lambda x: x[1])
                # max_dz_date, max_dz_count = max(dz.items(), key=lambda x: x[1])
                # max_dn_date, max_dn_count = max(dn.items(), key=lambda x: x[1])
                # print("正面数量最多的日期和数量：", max_dp_date, max_dp_count)
                # print("中性数量最多的日期和数量：", max_dz_date, max_dz_count)
                # print("负面数量最多的日期和数量：", max_dn_date, max_dn_count)
                # dp_str ="{}({})".format(max_dp_date,max_dp_count)
                # dz_str ="{}({})".format(max_dz_date,max_dz_count)
                # dn_str ="{}({})".format(max_dn_date,max_dn_count)
                # print(dp_str,dz_str,dn_str)
                # # 获取所有的日期（键）
                # dates = set(dp.keys()) | set(dz.keys()) | set(dn.keys())
                # # 找到最早和最晚的日期
                # earliest_date = min(dates)
                # latest_date = max(dates)
                # print("最早的日期：", earliest_date)
                # print("最晚的日期：", latest_date)
                # # 加载模板
                # doc = DocxTemplate(path+"\测试报告.docx")
                # # 创建一个字典，其中的键对应模板中的占位符
                # context = {"website": "微博",
                #         "keyword":keyword,
                #         "start_time":earliest_date,
                #         "end_time":latest_date,
                #         "positive_str":positive_str,
                #         "negative_str":negative_str,
                #         "dp_str":dp_str,
                #         "dz_str":dz_str,
                #         "dn_str":dn_str,
                #         "negatice":negative_str,
                #         }
                # # 填充模板
                # doc.render(context)
                # # 保存生成的报告
                # doc.save(path+"/report.docx")
                # convert(path+"/report.docx", path+"/report.pdf")
                # # 使用函数
                # file_path = path+'/report.pdf'  # 替换为你的PDF文件的本地路径
                # url_pdf = upload_file_to_0x0(file_path)
                # print('URL:', url_pdf)
                # st.session_state.url_pdf=url_pdf

                st.session_state.file_clean=file_clean
                clean_data = pd.read_csv(file_clean, encoding='utf-8', sep=';')
                st.write(' ')
                csv_clean_data = clean_data.to_csv(index=False)

                st.download_button("下载数据",csv_clean_data, file_name=downloadfile_name, mime='text/csv')        
                st.write(clean_data)


    if tabs == 'Regional Analysis':
        
        st.subheader("地域情感分析")
        if  st.session_state.file_in==" ":
            st.session_state.average_score=None
            waring=st.empty()
            waring=st.warning("请先获取并上传数据")
        # else:
        col1,col2=st.columns([3,1])
        
        with col1:
            with st.spinner('Wait about 20 seconds'):
                with st.expander("情绪地图",True):
                    if st.session_state.file_in ==" ":
                        unploaded_in = st.empty() 
                        uploaded_file2=unploaded_in.file_uploader("")
                        if uploaded_file2 is not None:
                            waring.empty()
                            st.session_state.file_in=uploaded_file2
                            st.success('upload success!')
                            # if st.session_state.website==" ":
                            st.session_state.website = st.selectbox('请选数据的地区范围:',(' ','国内', '世界'))
                            style=st.empty()
                            col,col_map,col=st.columns([1,8,1])
                            with col_map:
                                if st.session_state.website=="国内":
                                    # st.session_state.style=style.selectbox("  ",("标准情绪值","相对情绪值"))
                                    analysis('群体情绪中国地图',uploaded_file2)
                                if st.session_state.website=="世界":
                                    # st.session_state.style=style.selectbox("  ",("标准情绪值","相对情绪值"))
                                    analysis('群体情绪世界地图',uploaded_file2)
                                unploaded_in.empty()
                    else:
                        uploaded_file2=st.session_state.file_in
                        if st.session_state.website==" ":
                            st.session_state.website = st.selectbox('请选数据的地区范围:',(' ','国内', '世界'))
                        style=st.empty()
                        col,col_map,col=st.columns([1,8,1])
                        with col_map:
                            if st.session_state.website=="国内":
                                # st.session_state.style=style.selectbox("  ",("标准情绪值","相对情绪值"))
                                analysis('群体情绪中国地图',uploaded_file2)
                            if st.session_state.website=="世界":
                                # st.session_state.style=style.selectbox("  ",("标准情绪值","相对情绪值"))
                                analysis('群体情绪世界地图',uploaded_file2)
                if st.session_state.file_in !=" " and st.session_state.website!=" ":
                        with st.expander("各地区情绪占比",True):
                            b1, b2, b3 = st.columns([1, 0.3, 0.2])
                            with b1:
                                st.empty()
                            with b2:
                                st.session_state.p=st.selectbox("",("正面","负面"))
                            col,col_pie,col=st.columns([1,8,1])
                            with col_pie:
                                analysis("群体情绪强度饼图",uploaded_file2)
                

        with col2:
            if st.session_state.file_in !=" " and st.session_state.website!=" ":
                with st.expander('分析报告',True):
                    report_show()


    if tabs == 'Time Domain':
        # st.session_state.data=None
        st.subheader("时序情感分析")
        if st.session_state.file_in==" ":
            st.session_state.average_score=None
            waring=st.empty()
            waring=st.warning("请先获取并上传数据")
        # else:
        col1,col2=st.columns([3,1])
        with col1:
            with st.spinner('Wait about 10 seconds'):
                with st.expander("群体情绪趋势",True):
                    if st.session_state.file_in ==" ":
                        unploaded_in = st.empty() 
                        uploaded_file4=unploaded_in.file_uploader(" ")
                        if uploaded_file4 is not None:
                            waring.empty()
                            st.session_state.file_in=uploaded_file4
                            path1=get_middle_part(uploaded_file4.name)
                            
                            orifile=path1+"/"+path1.replace("数据", "")+'.csv'
                            # orifile="D:\电磁辐射网络舆情分析系统\code\微博日本核污水排放.csv"
                            
                            post_all,post_poster=find_imppost_data(uploaded_file4.name)
                            if "三胎" not in uploaded_file4.name:
                                st.session_state.post_url=match_url(post_poster,orifile)
                            else:
                                st.session_state.post_url=None
                            st.success('upload success!')       
                            analysis('群体情绪趋势图',uploaded_file4)
                            unploaded_in.empty()
                        
                            if st.session_state.data:
                                st.warning(st.session_state.data+" 的代表帖子")
                                st.warning(st.session_state.imppost[st.session_state.data])

                    else:
                        uploaded_file4=st.session_state.file_in
                        path1=get_middle_part(uploaded_file4.name)
                        
                        orifile=path1+"/"+path1.replace("数据", "")+'.csv'
                        
                        # orifile="D:\电磁辐射网络舆情分析系统\code\微博日本核污水排放.csv"
                        post_all,post_poster=find_imppost_data(uploaded_file4.name)
                        if "三胎" not in uploaded_file4.name:
                            st.session_state.post_url=match_url(post_poster,orifile)
                        else:
                            st.session_state.post_url=None
                        analysis('群体情绪趋势图',uploaded_file4)
                    
                        if st.session_state.data:
                            st.warning(st.session_state.data+" 的代表帖子")
                            st.warning(st.session_state.imppost[st.session_state.data])
                        
                        st.warning('点击查看各日期的代表帖子')
                             
        with col2:
            if st.session_state.file_in !=" ":
                with st.expander('分析报告',True):
                    report_show()
            

    if tabs == 'Comparative Ranking':
        st.session_state.p2="正面"
        video_path=" "
        st.subheader("多维度情感分析")
        if  st.session_state.file_in==" ":
            st.session_state.average_score=None
            waring=st.empty()
            waring=st.warning("请先获取并上传数据")
        col1,col2=st.columns([1,1])

        with col1:
            with st.expander("正负情绪排行榜",True):
                st.session_state.name=None
                st.session_state.p2 = None
                if st.session_state.file_in ==" ":
                    unploaded_in = st.empty() 
                    uploaded_file6=unploaded_in.file_uploader(" ")
                    if uploaded_file6 is not None:
                        st.session_state.file_in=uploaded_file6
                        waring.empty()
                        st.success('upload success!')
                        b1, b2 = st.columns([1, 0.3])
                        with b1:
                            st.empty()
                        with b2:
                            st.session_state.p2=st.selectbox("",("正面","负面"))
                        analysis('群体情绪排行榜',uploaded_file6)
                        unploaded_in.empty()
                else:
                    uploaded_file6=st.session_state.file_in
                    b1, b2 = st.columns([1, 0.3])
                    with b1:
                        st.empty()
                    with b2:
                        st.session_state.p2=st.selectbox("",("正面","负面"))
                    analysis('群体情绪排行榜',uploaded_file6)
            if st.session_state.p2 is not None:
                with st.expander('展开显示全部标题'):
                    if st.session_state.p2=="负面":
                        ln = len(st.session_state.title_N)
                        for j in range(0, ln):
                            st.write(str(j) + ': ' + st.session_state.title_N[j])
                    else:
                        ln = len(st.session_state.title_P)
                        for j in range(0, ln):
                            st.write(str(j) + ': ' + st.session_state.title_P[j])

        with col2:
            # with st.expander("媒介风格分析",True):
            #     if st.session_state.name!=None:
            #         warn=st.empty()
            #         warn.warning(st.session_state.name)
            #         if "的微博视频" in st.session_state.name:
            #             if'卫星观地球'in st.session_state.name:
            #                 video_path=r'data_weibo\日本核污水排放\video\1.mp4'    
            #             if'难舍深蓝'in st.session_state.name:
            #                 video_path=r'data_weibo\日本核污水排放\video\2.mp4'    
            #             if'经济过热'in st.session_state.name:
            #                 video_path=r'data_weibo\疫情后的经济\video\1.mp4'
            #             if'德国联邦议院'in st.session_state.name:
            #                 video_path=r'data_weibo\疫情后的经济\video\2.mp4'
            #             if'墨染诗婳'in st.session_state.name:
            #                 video_path=r'data_weibo\日本核污水排放\video\9.mp4'    

            #             result_emotion="result.txt"
            #             file_modality="C:/Users/86187/Desktop/新闻策划与效果评估系统/情感传播效果评估子系统/result_modality.csv"
                        
            #         col_video,col_charts=st.columns([1,1])                

            #         if video_path !=" ":
            #             other_video=st.empty()
            #             with col_video:
            #                 file_video=st.empty()
            #                 file_video.video(video_path) # 更改点                                

            #             with col_charts:                           
            #                 base_name = os.path.basename(video_path)
            #                 fn = os.path.splitext(base_name)[0]
            #                 try:
            #                     V2EM_prediction.main_for_st.emotion_analysis(str(fn)) 
            #                     the_chart=st.selectbox('',('情绪极性','各模态细粒度分析'))
            #                     if the_chart=='情绪极性':
            #                         analysis('单视频情绪极性',result_emotion)
            #                     if the_chart=='各模态细粒度分析':
            #                         analysis('单视频模态细粒度',file_modality)
            #                 except:
            #                     warn.error('该视频多模态情感分析失效，尝试上传其他视频（失效原因：视频中未出现人脸或出现多个人脸）')
            #                     file_video.empty()
            #                     uploaded_video = other_video.file_uploader('  ')
            #                     if uploaded_video is not None:
            #                         warn.success('上传成功！')
            #                         other_video.empty()
            #                         fn = uploaded_video.name.split('.')[0]
            #                         mp4_path = f'D:/电磁辐射网络舆情分析系统/code/data_weibo/日本核污水排放/video/{fn}.mp4'
            #                         file_video.video(mp4_path)
            #                         V2EM_prediction.main_for_st.emotion_analysis(str(fn)) 
            #                         the_chart=st.selectbox('',('情绪极性','各模态细粒度分析'))
            #                         if the_chart=='情绪极性':
            #                             analysis('单视频情绪极性',result_emotion)
            #                         if the_chart=='各模态细粒度分析':
            #                             analysis('单视频模态细粒度',file_modality)
          

            if st.session_state.file_in != " ":
                with st.expander('分析报告',True):
                    col,col_rpt,col=st.columns([1,2,1])
                    with col_rpt:
                        report_show()
                
            
    

if __name__ == '__main__':  # 不用命令端输入“streamlit run app.py”而直接运行
    if runtime.exists():
        main()
    else:
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())
