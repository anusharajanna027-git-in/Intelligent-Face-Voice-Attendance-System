import streamlit as st
from src.screens.home_screen import home_screen
from src.screens.teacher_screen import teacher_screen
from src.screens.student_screen import student_screen


def main():
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
            
main()