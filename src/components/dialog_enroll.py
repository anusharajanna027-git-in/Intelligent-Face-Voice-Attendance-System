import streamlit as st
from src.database.db import enroll_student_to_subject # importing the enroll_student_to_subject db fnx
from src.database.config import supabase

import time


@st.dialog("Enroll in Subject")
def enroll_dialog():
    st.write('Enter the subject code provided by your teacher to enroll')
    join_code = st.text_input('Subject Code', placeholder='Eg. CS101')

    if st.button('Enroll now', type='primary', width='stretch'):
        if join_code:
            #if the subject_codes presenet in the subjects table in db those subject_cose is qual with the current student entered for subj enrollement then return the subjects of what the student will tsubject enrollements
            res = supabase.table('subjects').select('subject_id, name, subject_code').eq('subject_code', join_code).execute()
            if res.data:
                subject = res.data[0]
                # next to  check if the student _id is already exised in the subject_students table
                student_id = st.session_state.student_data['student_id']#get the student data from the session_state
                #to check=> this particular student is exist in the subject_students table in db
                check = (
                    supabase.table('subject_students')
                    .select('*')
                    .eq('subject_id', subject['subject_id'])
                    .eq('student_id', student_id)
                    .execute()
                )
                if check.data:
                    st.warning('You are already enrolled in this program')
                else:
                    #if the subject is not exist then enroll know  by calling the db query
                    enroll_student_to_subject(student_id, subject['subject_id'])
                    st.success('Succesfully enrolled!')
                    time.sleep(1)
                    st.rerun()
            else:
                st.warning('Please enter a subject code')