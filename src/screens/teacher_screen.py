import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime
from src.database.config import supabase
from src.ui.style_base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.database.db import check_teacher_exist, create_teacher, teacher_login, get_teacher_subjects, get_attendance_for_teacher
from src.components.dialog_create_subject import create_subject_dialog
from src.components.subject_card import subject_card
from src.components.dialog_share_subject import share_subject_dialog
from src.components.dialog_add_photo import add_photos_dialog
from src.pipelines.face_pipeline import predict_attendance
from src.components.dialog_attendance_result import attendance_result_dialog
from src.components.dialog_voice_attendance import voice_attendance_dialog
def teacher_screen():

    style_background_dashboard()
    style_base_layout()

    # this condition is to check if the teacher is already logged in or not, if yes then show the dashboard else show the login or register screen
    if "teacher_data" in st.session_state:
        teacher_dashboard()
    #putting an condition to check if the teacher is in login or register mode and show the respective screen
    elif 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type=="login":
        teacher_screen_login()
    elif st.session_state.teacher_login_type=="register":
        teacher_screen_register()

# defining the teacher dashboard
def teacher_dashboard():
    teacher_data = st.session_state.teacher_data
    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        st.subheader(f"""Welcome, {teacher_data['name']}""")
        if st.button("Logout", type='secondary', key='loginbackbtn' ,shortcut="control+backspace"):
            st.session_state['is_logged_in']=False
            del st.session_state.teacher_data
            st.rerun()


    st.space()

    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab = 'take_attendance'
    #creat a 3 tabs of columns -Take Attendance,Manage Subjects,Attendance Records
    tab1, tab2, tab3 = st.columns(3)


    with tab1:
        type1 = "primary" if st.session_state.current_teacher_tab == 'take_attendance' else "tertiary"
        if st.button('Take Attendance',type=type1, width='stretch', icon=':material/ar_on_you:'):
            st.session_state.current_teacher_tab = 'take_attendance'
            st.rerun()

    with tab2:
        type2 = "primary" if st.session_state.current_teacher_tab == 'manage_subjects' else "tertiary"
        if st.button('Manage Subjects', type=type2, width='stretch', icon=':material/book_ribbon:'):
            st.session_state.current_teacher_tab = 'manage_subjects'
            st.rerun()

    with tab3:
        type3 = "primary" if st.session_state.current_teacher_tab == 'attendance_records' else "tertiary"
        if st.button('Attendance Records',type=type3, width='stretch', icon=':material/cards_stack:'):
            st.session_state.current_teacher_tab = 'attendance_records'
            st.rerun()

    st.divider()

    if st.session_state.current_teacher_tab == "take_attendance":
        teacher_tab_take_attendance()#once the teacher press take_attendence this fnx will render similarly those 2 
    if st.session_state.current_teacher_tab == "manage_subjects":
        teacher_tab_manage_subjects()
    if st.session_state.current_teacher_tab == "attendance_records":
        teacher_tab_attendance_records()

    
    footer_dashboard()
  #here defining the functions for those
#implementing the attendence
#1.attendence
def teacher_tab_take_attendance():
    teacher_id = st.session_state.teacher_data['teacher_id']
    st.header('Take AI Attendance')


    if 'attendance_images' not in st.session_state:
        st.session_state.attendance_images = []
    #first get the teachers available subjects
    subjects = get_teacher_subjects(teacher_id)

    if not subjects:# if not then must create
        st.warning('You havent created any subjects yet! Please create one to begin!')
        return
    
    #if subjects found==>>show them  like an selectbox structure
    subject_options = {f"{s['name']} - {s['subject_code']}": s['subject_id'] for s in subjects}

    # 2 columns=> one for to select subject and another for to add the photos
    col1, col2 = st.columns([3,1], vertical_alignment='bottom')

    with col1:
        selected_subject_label = st.selectbox('Select Subject', options=list(subject_options.keys()))

    with col2:
        if st.button('Add Photos', type='primary', icon=':material/photo_prints:', width='stretch'):
            add_photos_dialog()#defining the fnx

    # once the teacher selected the any subject through subject_options 
    selected_subject_id = subject_options[selected_subject_label]

    st.divider()

    # if once the images are availabe in session_state meanse teacher uploaded the photos those are appended to attendance_image
    # Represent(preiew) those images in an 4x4 grid
    if st.session_state.attendance_images:#check if images present in attendance_images
        st.header('Added Photos')
        gallery_cols = st.columns(4)#4 columns

        #one by one get the image from attendance_images
        for idx, img in enumerate(st.session_state.attendance_images):
            #make 4 columns distribution==>>meanse if 1 photo upload then it will store in 1st column and 2 nd photo in 2nd column and 3rd photo in 3rd column....
            with gallery_cols[idx % 4 ]:
                #adding image
                st.image(img, width='stretch', caption=f'Photo {idx+1}')
    has_photos = bool(st.session_state.attendance_images) #if images are present in the attendance_images then it returns true or if empty it returns false

    #creating 3 columns
    c1, c2, c3 = st.columns(3)

    #clear all photos
    with c1:
        if st.button('Clear all photos', width='stretch', type='tertiary', icon=':material/delete:', disabled=not has_photos):
            st.session_state.attendance_images = []
            st.rerun()

    #run face analysis
    with c2:
        
        if st.button('Run Face Analysis', width='stretch', type='secondary', icon=':material/analytics:', disabled=not has_photos):
            with st.spinner('Deep scanning classroom photos...'):
                all_detected_ids = {}

                for idx, img in enumerate(st.session_state.attendance_images):
                    img_np = np.array(img.convert('RGB'))#convert the image to np array and also to RGB Channels
                    detected, _, _ = predict_attendance(img_np)

                    # if the image detected
                    if detected:
                        for sid in detected.keys():
                            student_id = int(sid)# whatever the students detected in image then they will store in the student_id column
                            # append the photos along with the student_id to all_detected_ids
                            all_detected_ids.setdefault(student_id, []).append(f"Photo {idx+1}")
                #enrolled response => whatever the students under the subjects, get the  all students which equals to selected_subject_id 
                enrolled_res = supabase.table('subject_students').select("*, students(*)").eq('subject_id',selected_subject_id ).execute()
                enrolled_students = enrolled_res.data
                #if not stduents exist under the select subject
                if not enrolled_students:
                    st.warning('No students enrolled in this course')
                else:
                    #if students exist=>attendence logs are show in pandas table and also store it in a db
                    results, attendance_to_log  = [], []
                    # to get current timestamp=>>using datetime.now()
                    current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

                    #whatever the students for those to run a loop
                    for node in enrolled_students:
                        #put the students in a temproary variable student
                        student = node['students']
                        sources = all_detected_ids.get(int(student['student_id']), [])
                        is_present= len(sources) > 0

                        results.append({
                            "Name": student['name'],
                            "ID": student['student_id'],
                            "Source": ", ".join(sources) if is_present else "-",
                            "Status": "✅ Present" if is_present else "❌ Absent"
                        })

                        attendance_to_log.append({
                            'student_id': student['student_id'],
                            'subject_id': selected_subject_id,
                            'timestamp': current_timestamp,
                            'is_present': bool(is_present)
                        })
                #results and attendance are shown it in a pdandas dataframe for that we define a function 
                attendance_result_dialog(pd.DataFrame(results), attendance_to_log)
    # voice attendence
    with c3:
        if st.button('Use Voice Attendance', type='primary', width='stretch', icon=':material/mic:'):
            voice_attendance_dialog(selected_subject_id)

#2.Manage Subjects            
def teacher_tab_manage_subjects():
    #to get the teacher
    teacher_id = st.session_state.teacher_data['teacher_id']
    col1, col2 = st.columns(2)
    with col1:
        st.header('Manage Subjects', width='stretch')

    with col2:
        #once the button clicked for to create subjects then the following fnx call
        if st.button('Create New Subject', width='stretch'):
            create_subject_dialog(teacher_id)

    # LIST all SUBJECTS
    subjects = get_teacher_subjects(teacher_id)# getting the subject teachers
    if subjects:
        for sub in subjects:
            stats = [
                ("🫂", "Students", sub['total_students']),
                ("🕰️", "Classes", sub['total_classes']),
            ]
        #share button create
        def share_btn():
            if st.button(f"Share Code: {sub['name']}", key=f"share_{sub['subject_code']}", icon=":material/share:"):
                share_subject_dialog(sub['name'], sub['subject_code'])
            st.space()
        # create subject card
        subject_card(
            name = sub['name'],
            code = sub['subject_code'],
            section = sub['section'],
            stats=stats,
            footer_callback=share_btn
        )
    else:
        st.info("NO SUBJECTS FOUND. CREATE ONE ABOVE")
    
#3. Attendance Records
def teacher_tab_attendance_records():
    st.header('Attendance Records')

    teacher_id = st.session_state.teacher_data['teacher_id']

    records = get_attendance_for_teacher(teacher_id)#from db 

    if not records:
        return
    
    data = []

    for r in records:
        ts = r.get('timestamp')

        data.append({
            "ts_group": ts.split(".")[0] if ts else None,
            "Time": datetime.fromisoformat(ts).strftime("%Y-%m-%d %I:%M %p") if ts else "N'A",
            "Subject": r['subjects']['name'],
            "Subject Code":r['subjects']['subject_code'],
            "is_present": bool(r.get('is_present', False))
        })

    # compute/shown in pandas
    df = pd.DataFrame(data)



    summary = (
        df.groupby(['ts_group', 'Time', 'Subject', 'Subject Code'])
        .agg(
            Present_Count = ('is_present', 'sum'),
            Total_Count =('is_present', 'count')
        ).reset_index()

    )

    summary['Attendance Stats'] = (
        "✅ " + summary['Present_Count'].astype(str) + " /"
        + summary['Total_Count'].astype(str) + ' Students'
    )

    display_df = ( summary.sort_values(by='ts_group' ,ascending=False)
                  [['Time', 'Subject', 'Subject Code', 'Attendance Stats']]
                  )
    
    st.dataframe(display_df, width='stretch', hide_index=True)

    
    

#defining the  teacher login
def login_teacher(username, password):
    if not username or not password:
        return False

    teacher = teacher_login(username, password)# callinh the teacher_login function from db.py to check if the username and password match with the database
    if teacher:
        st.session_state.user_role = 'teacher'
        st.session_state.teacher_data = teacher
        st.session_state.is_logged_in = True
        return True
    return False


# 2 fnx to build teacher login and register
def teacher_screen_login():
    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go back to Home", type='secondary', key='loginbackbtn' ,shortcut="control+backspace"):
            st.session_state['teacher_login_type']=None
            st.rerun()

    st.header('Login using password', text_alignment='center')
    st.space()
    st.space()

    teacher_username = st.text_input("Enter username", placeholder='anusha')
    
    teacher_pass = st.text_input("Enter password", placeholder='anusha')

    st.divider()

    btnc1, btnc2 = st.columns(2)

    with btnc1:
        if st.button("Login", icon=':material/passkey:', shortcut='control+enter', width='stretch'):
            if login_teacher(teacher_username, teacher_pass):
                st.toast(f"Welcome back {teacher_username}!", icon="👋") # toast => its like a flash message which will show for a few seconds and then disappear
                import time
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid username or password")


    with btnc2:
        if st.button("Register Instead", icon=':material/passkey:', width='stretch'):
            st.session_state.teacher_login_type="register"
            st.rerun()

    footer_dashboard()

# here we will define the register_teacher function to register the teacher and store the data in the database
def register_teacher(teacher_username, teacher_name, teacher_pass, teacher_pass_confirm):
    if not teacher_username or not teacher_name or not teacher_pass:
        return False, "All fields are required"
    if check_teacher_exist(teacher_username):
        return False, "Username already exists"
    if teacher_pass != teacher_pass_confirm:
        return False, "Passwords doesn't match"

    try:
        create_teacher(teacher_username, teacher_pass, teacher_name)
        return True, "Successfully Created! Login Now"
    except Exception as e:
        return False, "Unexpected Error!"




def teacher_screen_register():
    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go back to Home", type='secondary', key='loginbackbtn' ,shortcut="control+backspace"):
            st.session_state['teacher_login_type']=None
            st.rerun()

    st.header('Register your teacher profile', text_alignment='center')

    st.space()
    st.space()

    teacher_username = st.text_input("Enter username", placeholder='anusha')
    teacher_name = st.text_input("Enter name", placeholder='Anusha R')
    teacher_pass = st.text_input("Enter password", placeholder='anusha')
    teacher_pass_confirm = st.text_input("Confirm password", type='password', placeholder='anusha')
    
    st.divider()

    btnc1, btnc2 = st.columns(2)

    with btnc1:
        if st.button("Register Now", icon=':material/passkey:', shortcut='control+enter', width='stretch'):
            success, message = register_teacher(teacher_username, teacher_name, teacher_pass, teacher_pass_confirm)
            if success:
                st.success(message)
                import time
                time.sleep(2)
                st.session_state.teacher_login_type="login"
                st.rerun()
            else:
                st.error(message)

    with btnc2:
        if st.button("Login Instead", icon=':material/passkey:', width='stretch'):
            st.session_state.teacher_login_type="login"
            st.rerun()

    st.header('Register your teacher profile', text_alignment='center')
