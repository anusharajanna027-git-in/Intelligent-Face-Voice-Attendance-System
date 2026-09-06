#important note
#pipeline(1.Face Image==>>2.Face Detector(dlib)==>>3.Shape Predictor(sp)->landmarks(68 are there)==>>4.ResNet(facerec)->embedding(128D))
# we detect using the SVM Classifier=>pipeline(1.FaceImage=>>2.ResNet(feature ectractor)=>>3.128D embedding(face detector)=>>4.SVM(classifier)=>>5.StudentID)

import dlib # dlib will provide 3 way of models =>1st is face for  to make a bounding box around the faceand detect the face not detect the landmarks only face first, 2nd is shape predictor(sp) will detect the face landmarks and 3rd is ResNet(face recognizer) to get the embeddings of the face
import numpy as np
import face_recognition_models
from sklearn.svm import SVC
import streamlit as st

from src.database.db import get_all_students

# now we build the 3 models using dlib and face_recognition_models library and then we will use those models to build the pipeline for the face recognition system
@st.cache_resource# data is in cache=>this is for once load is enough and then we can use it multiple times without loading it again and again
def load_dlib_models():
    #detector model
    detector = dlib.get_frontal_face_detector()# this is the face detector model which will detect the face in the image and then we will use this face to detect the landmarks and then we will use those landmarks to get the embeddings of the 
    #shape predictor model-detect landmarks
    sp = dlib.shape_predictor(
        face_recognition_models.pose_predictor_model_location()
    )
    #resnet model(face recogniser model)
    facerec = dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )
    return detector, sp, facerec

#now we define a fnx to  get the embeddings using numpy image  by using the 3 models
def get_face_embeddings(image_np):
    detector, sp, facerec = load_dlib_models()#loading the 3 modls
    # whatever the faces apperars in the image need to detect those also and onebyone gets inside the forloop to get each face_descriptors #detecting the face in the image using the detector model
    faces = detector(image_np, 1)
    
    encodings = []#all embedddings store in array

    for face in faces:
        shape = sp(image_np, face)#detecting the landmarks of the face using the shape predictor model
        face_descriptor = facerec.compute_face_descriptor(image_np, shape, 1)#getting the embeddings of the face using the ResNet model
        encodings.append(np.array(face_descriptor))
    return encodings

@st.cache_resource
def get_trained_model():
    X = [] # embeddings
    y = [] #ids

    #if students are present in the database then get all the students
    student_db = get_all_students()

    #if not students there return None
    if not student_db:
        return None
    #then if present get all the embeddings
    for student in student_db:
        embedding = student.get('face_embedding')#get embeddings from the above models and then store in the X array and then get the student id and store in the y array
        if embedding:
            X.append(np.array(embedding))#embeddings stored in X
            y.append(student.get('student_id'))#ids stored in y

    if len(X) ==0:
        return 0

    #defining the svc classifier ml model to train the embeddings and then use that model to predict the student id using the embeddings
    clf = SVC(kernel='linear', probability=True, class_weight='balanced')

    try:
        clf.fit(X, y)
    except ValueError:
        pass

    return {'clf': clf, 'X':X, "y":y}

  #train the classfier
def train_classifier():
    st.cache_resource.clear()
    model_data = get_trained_model()
    return bool(model_data)

def predict_attendance(class_image_np):
    encodings = get_face_embeddings(class_image_np)

    detected_student = {}


    model_data = get_trained_model()

    if not model_data:
        return detected_student, [], len(encodings)
    
    clf = model_data['clf']
    X_train = model_data['X']
    y_train = model_data['y']

    all_students = sorted(list(set(y_train)))#list of studenets in a sorted array

    for encoding in encodings:
        if len(all_students)>= 2:
            # we find the predicted id using classifier
            predicted_id= int(clf.predict([encoding])[0])
        else:
            predicted_id = int(all_students[0])

        #once the classifier tell the id as "this  is the id of that student" 
        # then get the embedding of that student from tained X
        student_embedding = X_train[y_train.index(predicted_id)]
        #bbest match score
        best_match_score = np.linalg.norm(student_embedding - encoding)

        resemblance_threshold = 0.6

        if best_match_score <= resemblance_threshold:
            detected_student[predicted_id] = True
    return detected_student, all_students, len(encodings)


# predicted_id

# Suppose your model receives a new face:

# encoding

# and predicts:

# predicted_id = 5

# This means:

# "I think this face belongs to student ID 5."

# 2. y_train.index(predicted_id)

# Your training data might look conceptually like:

# X_train                         y_train

# face_embedding_0  ----------->  2
# face_embedding_1  ----------->  7
# face_embedding_2  ----------->  5
# face_embedding_3  ----------->  3

# If:

# predicted_id = 5

# then:

# y_train.index(5)

# returns:

# 2

# because student ID 5 is at index 2.

# 3. X_train[y_train.index(predicted_id)]

# Now:

# X_train[2]

# gets the embedding corresponding to student ID 5.

# So:

# student_embedding = X_train[y_train.index(predicted_id)]

# means:

# Get the training face embedding that belongs to the student predicted by the model.

# For example:

# predicted_id = 5

#        ↓
# find ID 5 in y_train

#        ↓
# index = 2

#        ↓
# X_train[2]

#        ↓
# student_embedding
# 4. Now the important part 👇
# student_embedding - encoding

# You have two embeddings:

# student_embedding = stored/training face
# encoding          = new/current face

# For example, imagine a tiny 3-dimensional embedding:

# student_embedding = [0.2, 0.7, 0.4]

# encoding          = [0.3, 0.6, 0.5]

# Subtract them:

# [0.2, 0.7, 0.4]
# -
# [0.3, 0.6, 0.5]
# ----------------
# [-0.1, 0.1, -0.1]
# 5. np.linalg.norm()

# Then:

# np.linalg.norm(student_embedding - encoding)

# calculates the Euclidean distance between the two embeddings.

# Conceptually:

# distance = √((-0.1)² + (0.1)² + (-0.1)²)

# which is approximately:

# 0.173

# So:

# best_match_score = 0.173
# set a threshold=0.6
# bestscore >0.6,then large differ in face or then best score is less than the threshold then then face matches

# Smaller distance = faces are more similar.

# The exact threshold depends on how your face embeddings/model are generated.

# So your complete logic is:
# New face
#    ↓
# encoding
#    ↓
# Model predicts student ID
#    ↓
# predicted_id
#    ↓
# Find that student's stored embedding
#    ↓
# student_embedding
#    ↓
# Compare stored embedding with new encoding
#    ↓
# Euclidean distance
#    ↓
# best_match_score
#    ↓
# threshold=0.6
#    ↓
#  >0.6=>face diff  or <0.6=>face match

# In one sentence:

# Your model first says "I think this is Student 5", then this code checks how close the new face actually is to Student 5's stored face embedding.

# This second distance check is useful because a prediction alone doesn't tell you how confident the face match is.
