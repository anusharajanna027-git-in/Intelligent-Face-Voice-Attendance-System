import streamlit as st
from src.components.header import header_home
from src.ui.style_base_layout import style_background_home, style_background_dashboard, style_base_layout
from src.components.footer import footer_home
def home_screen():

    header_home()#calling the header function we already defined in the header.py

    style_base_layout()
    style_background_dashboard()
    style_background_home()# calling the style hearder 
    
    

    col1, col2 = st.columns(2, gap="Large")

    with col1:
        st.header("I'm Student")
        st.image("https://i.ibb.co/844D9Lrt/mascot-student.png", width=120)
        if st.button('Student Portal', type='primary', icon=':material/arrow_outward:', icon_position='right'):
            st.session_state['login_type']='student'
            st.rerun()
    with col2:
        st.header("I'm Teacher")
        st.image("https://i.ibb.co/CsmQQV6X/mascot-teacher.png", width=120)
        if st.button('Teacher Portal', type='primary', icon=':material/arrow_outward:', icon_position='right'):
            st.session_state['login_type']='teacher'# once the the user click on teacher portal buttion then login_type becomes change to teacher
            st.rerun()
    footer_home()