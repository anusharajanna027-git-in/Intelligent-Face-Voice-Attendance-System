import streamlit as st
from src.screens.home_screen import home_screen
from src.screens.teacher_screen import teacher_screen
from src.screens.student_screen import student_screen
from src.components.dialog_auto_enrol import auto_enroll_dialog

def main():
    st.set_page_config(
        page_title = 'SnapClass - Making Attendance faster using AI',
        page_icon = "https://i.ibb.co/YTYGn5qV/logo.png"
    )
    #Statefulness in Streamlit = maintaining data/values across script reruns during a user's session.Common things stored in st.session_state=>Login status ,Selected options,Counters,Uploaded files,Chat history,User information,ML model outputs
    #for example=>chat history remains available even though Streamlit reruns the script.
    if 'login_type' not in st.session_state:
        st.session_state['login_type']=None# initialize the login_type be none in this case the home page will show initially

    match st.session_state['login_type']:
        case 'teacher':# if teacher logsin then show a teacher dashboard
            teacher_screen()
        case 'student':# if student logsin then show a student dashboard
            student_screen()
        case None:
            home_screen()# otherwiae show the home page

    #quick enrollement implementing using qr code (url)
    # join_code is detected in url then it will convert this in student login side if they already logged then show the auto_enroll_dialog
    join_code = st.query_params.get('join-code') # to get the join code from url of teacher side
    if join_code:
        if st.session_state.login_type != 'student':
            st.session_state.login_type = 'student'
            st.rerun()
        if st.session_state.get('is_logged_in') and st.session_state.get('user_role') == 'student':
            auto_enroll_dialog(join_code)
            
main()