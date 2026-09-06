import streamlit as st
from src.database.db import enroll_student_to_subject
from src.database.config import supabase
from PIL import Image
import time


@st.dialog("Capture or upload photos")
def add_photos_dialog():

    st.write('Add classroom photos to scan for attendance')

    # creating a photo tab it includes 2 tabs 
    # initializing the photo_tab if the tab is not in the session_state
    if 'photo_tab' not in st.session_state:
        st.session_state.photo_tab = 'camera'#camera opens
    #2 colums(2 tabs)
    t1, t2 = st.columns(2)

    #to show camera to click the photo
    with t1:
        type_camera = "primary" if st.session_state.photo_tab == 'camera' else 'tertiary'
        if st.button('Camera', type=type_camera, width='stretch'):
            st.session_state.photo_tab = 'camera'

    # to upload the photos
    with t2:
        type_upload = "primary" if st.session_state.photo_tab == 'upload' else 'tertiary'
        if st.button('Upload photos', type=type_upload, width='stretch'):
            st.session_state.photo_tab = 'upload'

    #camera opens - to capture the photo
    if st.session_state.photo_tab == 'camera':
        cam_photo = st.camera_input('Take Snapshot', key='dialog_cam')
        if cam_photo:
            # append the these captured images to attendance_images=> before the image to append parse those images using the PIL Library then append to attendence_images
            st.session_state.attendance_images.append(Image.open(cam_photo))
            st.toast('Photo Captured')
            st.rerun()

    # click to upload then opens the files =>select and upload
    if st.session_state.photo_tab == 'upload':
        uploaded_files = st.file_uploader( 'choose image files', type=['jpg', 'png', 'jpeg' ], accept_multiple_files=True, key='dialog_upload')
         #once upload
        if uploaded_files:
            for f in uploaded_files:
                #append those uploaded photos to attendance_images
                st.session_state.attendance_images.append(Image.open(f))
            
            st.toast('Photo Uploaded Successfully')
            st.rerun()

    st.divider()
    if st.button('Done', type='primary', width='stretch'):
        st.rerun()
