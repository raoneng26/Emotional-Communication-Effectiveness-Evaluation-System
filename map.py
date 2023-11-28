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
from streamlit_card import card
import base64
from streamlit_elements import elements, dashboard, mui, html,media
from streamlit import runtime
import sys
from streamlit.web import cli as stcli


# 创建一个仪表板对象
def main():
# You can create a draggable and resizable dashboard using
# any element available in Streamlit Elements.
    reportpath="report.jpg"
    with open(reportpath, "rb") as f:
        data = f.read()
        encoded = base64.b64encode(data)
        data = "data:image/png;base64," + encoded.decode("utf-8")
        with elements('dashboard'):

            # First, build a default layout for every element you want to include in your dashboard

            layout = [
                # Parameters: element_identifier, x_pos, y_pos, width, height, [item properties...]
                dashboard.Item("first_item", 0, 0, 2, 2),
                dashboard.Item("second_item", 0, 2, 2, 2,isDraggable=True, moved=False), 
                dashboard.Item('third_item',3,0,2,2),
            ]

            # Next, create a dashboard layout using the 'with' syntax. It takes the layout
            # as first parameter, plus additional properties you can find in the GitHub links below.

            with dashboard.Grid(layout):
                mui.Paper("First item", key="first_item")
        
                html.Img( src = data,href="https://www.youtube.com/watch?v=iik25wqIuFo",controls=True,key="second_item") 
                media.Player(url="https://www.youtube.com/watch?v=iik25wqIuFo", controls=True, key="third_item")
    

            # If you want to retrieve updated layout values as the user move or resize dashboard items,
            # you can pass a callback to the onLayoutChange event parameter.

            def handle_layout_change(updated_layout):
                print(updated_layout)

            with dashboard.Grid(layout, onLayoutChange=handle_layout_change):
                mui.Paper("First item", key="first_item")
                html.Img( src = data,href="https://www.youtube.com/watch?v=iik25wqIuFo",controls=True,key="second_item") 

                media.Player(url="https://www.youtube.com/watch?v=iik25wqIuFo", controls=True, key="third_item")  # 在仪表盘上添加一个图片元素，设置点击事件为打开一个新网页


# #    4.可拖动且可调整大小的仪表板
#     with elements("dashboard"):

#         # You can create a draggable and resizable dashboard using
#         # any element available in Streamlit Elements.

#         from streamlit_elements import dashboard

#         # First, build a default layout for every element you want to include in your dashboard

#         layout = [
#             # Parameters: element_identifier, x_pos, y_pos, width, height, [item properties...]
#             dashboard.Item("first_item", 0, 0, 2, 2),
#             dashboard.Item("second_item", 2, 0, 2, 2, isDraggable=False, moved=False),
#             dashboard.Item("third_item", 0, 2, 1, 1, isResizable=False),
#         ]

#         # Next, create a dashboard layout using the 'with' syntax. It takes the layout
#         # as first parameter, plus additional properties you can find in the GitHub links below.

#         with dashboard.Grid(layout):
#             mui.Paper("First item", key="first_item")
#             mui.Paper("Second item (cannot drag)", key="second_item")
#             mui.Paper("Third item (cannot resize)", key="third_item")

#         # If you want to retrieve updated layout values as the user move or resize dashboard items,
#         # you can pass a callback to the onLayoutChange event parameter.

#         def handle_layout_change(updated_layout):
#             # You can save the layout in a file, or do anything you want with it.
#             # You can pass it back to dashboard.Grid() if you want to restore a saved layout.
#             print(updated_layout)

#         with dashboard.Grid(layout, onLayoutChange=handle_layout_change):
#             mui.Paper("First item", key="first_item")
#             mui.Paper("Second item (cannot drag)", key="second_item")
#             mui.Paper("Third item (cannot resize)", key="third_item")



if __name__ == '__main__':  # 不用命令端输入“streamlit run app.py”而直接运行
    if runtime.exists():
        main()
    else:
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())