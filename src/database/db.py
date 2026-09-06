from src.database.config import supabase # importing the supabase instance here to write the quieries
import bcrypt


#hashing the password before storing it in the database
def hash_pass(pwd):
    return bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()

# checking the password with the hashed password stored in the database
def check_pass(pwd, hashed):
    try:
        return bcrypt.checkpw(pwd.encode(), hashed.encode())
    except (ValueError, TypeError):
        return False

# to check for unique username, returns false when username is already taken
def check_teacher_exist(username):
    response = supabase.table("teachers").select("username").eq("username", username).execute()
    return len(response.data) > 0


#creating the teachers and inserting them into the database
def create_teacher(username, password, name):
    hashed_password = hash_pass(password)
    data = {"username" : username, "password" : hashed_password, "name" : name}
    response = supabase.table("teachers").insert(data).execute()
    return response

#teacher login function to check if the username and password match with the database
def teacher_login(username, password):
    response = supabase.table("teachers").select("*").eq("username", username).execute()
    #if user exists
    if response.data:
        teacher = response.data[0]
        #check if the password matches
        if check_pass(password, teacher["password"]):# for hashing we use same algorithm due to this the password already stored during the registered and the the password what the user use the same during the login it becomes same when usimg the same algo it produces same hashing password then match the password and return the teacher data for this we define a function check_pass to check the password
            return teacher
    return None

def get_all_students():
     response = supabase.table("students").select("*").execute()
     return response.data

def create_student(new_name,face_embedding=None,voice_embedding=None):
    data = {'name': new_name,'face_embedding':face_embedding,'voice_embedding': voice_embedding}
    response = supabase.table('students').insert(data).execute()
    return response.data


def create_subject(subject_code,name,section,teacher_id):
    data = {"subject_code":subject_code,"name":name,"section":section,"teacher_id":teacher_id}
    response = supabase.table('subjects').insert(data).execute()
    return response.data

def get_teacher_subjects(teacher_id):
    response = supabase.table("subjects").select("*, subject_students(count), attendance_logs(timestamp)").eq("teacher_id", teacher_id).execute()
    subjects = response.data

    for sub in subjects:
        sub['total_students'] = sub.get("subject_students", [{}])[0].get('count', 0) if sub.get('subject_students') else 0
        attendance = sub.get('attendance_logs', [])
        # to get unique timestamps
        unique_sessions = len(set(log['timestamp'] for log in attendance))
        sub['total_classes'] = unique_sessions


        sub.pop('subject_student', None)
        sub.pop('attendance_logs', None)

    return subjects

#for student enrollement for the subjects under the table of subject_students 
def  enroll_student_to_subject(student_id, subject_id):
    data = {'student_id': student_id, "subject_id": subject_id}
    response= supabase.table('subject_students').insert(data).execute()
    return response.data

# to unenrollment of subejcts(is the student are already existed in the subject_students table then remove that student)
def  unenroll_student_to_subject(student_id, subject_id):
    response= supabase.table('subject_students').delete().eq('student_id', student_id).eq('subject_id', subject_id).execute()
    return response.data


# to get the subjects which enrolled by students
def get_student_subjects(student_id):
    response = supabase.table('subject_students').select('*, subjects(*)').eq('student_id', student_id).execute()
    return response.data

# to get the student attendance
def get_student_attendance(student_id):
    response = supabase.table('attendance_logs').select('*, subjects(*)').eq('student_id', student_id).execute()
    return response.data


def create_attendance(logs):
    response = supabase.table('attendance_logs').insert(logs).execute()
    return response.data

def get_attendance_for_teacher(teacher_id):
    response = supabase.table('attendance_logs').select("*, subjects!inner(*)").eq('subjects.teacher_id', teacher_id).execute()
    return response.data

