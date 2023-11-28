from st_on_hover_tabs import on_hover_tabs
import streamlit as st
from streamlit import runtime
import sys
from streamlit.web import cli as stcli

def main():
    st.set_page_config(layout="wide")

    st.header("Custom tab component for on-hover navigation bar")
    st.markdown('<style>' + open('./style.css').read() + '</style>', unsafe_allow_html=True)


    with st.sidebar:
        tabs = on_hover_tabs(tabName=['Start', 'Regional Analysis', 'Time Domain', 'Comparative Ranking'], 
                            iconName=['star', 'language', 'schedule', 'leaderboard'], default_choice=0)

    if tabs =='Start':
        st.title("Navigation Bar")
        st.write('Name of option is {}'.format(tabs))

    elif tabs == 'Regional Analysis':
        st.title("Paper")
        st.write('Name of option is {}'.format(tabs))

    elif tabs == 'Time Domain':
        st.title("Tom")
        st.write('Name of option is {}'.format(tabs))

    elif tabs == 'Comparative Ranking':
        st.title("Tom")
        st.write('Name of option is {}'.format(tabs))
    

if __name__ == '__main__':  # 不用命令端输入“streamlit run app.py”而直接运行
    if runtime.exists():
        main()
    else:
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())