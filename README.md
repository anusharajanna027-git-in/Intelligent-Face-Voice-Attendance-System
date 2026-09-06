# 🎓 SnapClass

## AI-Powered Face & Voice Attendance Management System

> **Smart Attendance. Secure Identity. Seamless Classroom Management.**

SnapClass is an **AI-powered attendance management software** designed to automate student attendance using **Face Recognition and Voice Recognition**.

The system combines **Computer Vision, Audio Processing, Machine Learning, QR-based subject enrollment, Streamlit, and Supabase** to provide a modern and efficient attendance platform for educational environments.

SnapClass eliminates the need for traditional manual attendance methods by allowing students to be identified through their biometric characteristics and automatically recording attendance in the database.

---

# 📖 About SnapClass

Traditional classroom attendance is usually performed through manual roll calls, paper records, or manually maintained digital spreadsheets.

These approaches can lead to:

* ⏱️ Loss of valuable classroom time
* ❌ Human errors
* 📝 Manual record maintenance
* 👥 Proxy attendance
* 🔄 Repetitive administrative work
* 📊 Difficulty managing attendance across multiple subjects

**SnapClass** provides an automated alternative using biometric identity recognition.

The platform allows teachers to create subjects and generate a **QR code or enrollment URL**. Students can use the QR code to enroll in the respective subject.

Once enrolled, students can register their biometric information and use **face or voice recognition** for identity verification during attendance.

---

# 🎯 Problem Statement

Educational institutions need an attendance system that is:

* Fast
* Reliable
* Easy to use
* Difficult to manipulate
* Easy to maintain
* Scalable
* Secure

Manual attendance systems do not always satisfy these requirements.

SnapClass addresses these challenges by combining **AI-based biometric recognition with automated database management**.

---

# 💡 Solution

SnapClass introduces a biometric attendance workflow:

```text
Student
   │
   ▼
Subject Enrollment
   │
   ▼
Biometric Registration
   │
   ├───────────────┐
   ▼               ▼
Face             Voice
Recognition      Recognition
   │               │
   ▼               ▼
Feature          Feature
Extraction       Extraction
   │               │
   └───────┬───────┘
           ▼
     ML Classification
           │
           ▼
   Student Identification
           │
           ▼
   Attendance Validation
           │
           ▼
      Supabase Database
```

---

# ✨ Key Features

## 👤 Face Recognition

SnapClass provides an AI-based face recognition pipeline for identifying registered students.

The pipeline includes:

* Face detection
* Face preprocessing
* Facial feature extraction
* Face embedding generation
* Machine learning classification
* Student identity prediction
* Attendance validation

---

## 🎙️ Voice Recognition

SnapClass also supports speaker recognition using voice input.

The voice pipeline uses:

* Audio recording
* Audio preprocessing
* Librosa
* Resemblyzer
* Speaker embeddings
* SVM classification
* Identity prediction

The system converts voice input into a numerical representation that can be processed by the machine learning classifier.

---

## 🤖 SVM-Based Classification

SnapClass uses a **Support Vector Machine (SVM)** classifier for biometric identity classification.

The classifier receives extracted biometric embeddings as input and predicts the corresponding registered student.

General workflow:

```text
Biometric Input
       │
       ▼
Preprocessing
       │
       ▼
Feature Extraction
       │
       ▼
Embedding
       │
       ▼
SVM Classifier
       │
       ▼
Predicted Student
       │
       ▼
Attendance
```

---

# 🧠 Face Recognition Pipeline

The face recognition system follows a multi-stage processing pipeline.

```text
Camera / Image Input
        │
        ▼
   Face Detection
        │
        ▼
Face Preprocessing
        │
        ▼
Feature Extraction
        │
        ▼
Face Embedding
        │
        ▼
SVM Classification
        │
        ▼
Student Identity
        │
        ▼
Attendance Validation
```

### Step 1 — Face Input

The system receives an image or camera frame containing the student's face.

### Step 2 — Face Detection

Dlib-based processing is used to detect the face from the input image.

### Step 3 — Preprocessing

The detected face is prepared for feature extraction.

### Step 4 — Feature Extraction

Relevant facial characteristics are converted into numerical representations.

### Step 5 — Embedding

The facial characteristics are represented as an embedding that can be used by the machine learning model.

### Step 6 — Classification

The embedding is passed to the trained SVM classifier.

### Step 7 — Identity Prediction

The classifier predicts the identity associated with the biometric representation.

### Step 8 — Attendance

After successful verification, the system records the student's attendance.

---

# 🎙️ Voice Recognition Pipeline

The voice recognition pipeline processes a student's speech/audio input.

```text
Microphone
    │
    ▼
Audio Recording
    │
    ▼
Audio Preprocessing
    │
    ▼
Librosa
    │
    ▼
Resemblyzer
    │
    ▼
Speaker Embedding
    │
    ▼
SVM Classifier
    │
    ▼
Student Identity
    │
    ▼
Attendance Validation
```

### Audio Processing

**Librosa** is used for processing and analyzing audio signals.

Depending on the processing pipeline, operations can include:

* Audio loading
* Sampling
* Signal preprocessing
* Audio normalization
* Feature preparation

### Speaker Embedding

**Resemblyzer** is used to generate a speaker representation from the voice input.

The resulting embedding provides a numerical representation of speaker characteristics.

### Classification

The generated embedding is passed to the trained SVM classifier to identify the registered student.

---

# 🤖 Machine Learning Architecture

The recognition architecture separates biometric processing from identity classification.

```text
                INPUT
                  │
        ┌─────────┴─────────┐
        │                   │
      IMAGE               AUDIO
        │                   │
        ▼                   ▼
      Dlib              Librosa
        │                   │
        ▼                   ▼
Face Features        Resemblyzer
        │                   │
        ▼                   ▼
Face Embedding       Voice Embedding
        │                   │
        └─────────┬─────────┘
                  ▼
             SVM Model
                  │
                  ▼
          Student Prediction
```

This approach allows the biometric feature extraction stage and classification stage to remain logically separated.

---

# 📱 QR-Based Subject Enrollment

SnapClass provides a convenient QR-based enrollment mechanism.

Instead of manually entering subject information, teachers can generate an enrollment QR code.

### Enrollment Flow

```text
Teacher
   │
   ▼
Create Subject
   │
   ▼
Generate QR Code
   │
   ▼
Share QR / URL
   │
   ▼
Student Scans QR
   │
   ▼
Subject Enrollment
   │
   ▼
Student Linked to Subject
```

This makes subject enrollment faster and more convenient.

---

# 👨‍🏫 Teacher Module

The teacher module is responsible for classroom and subject management.

### Teacher capabilities

* Teacher login/access
* Create subjects
* Select subjects
* Generate enrollment QR codes
* Share enrollment URLs
* Manage enrolled students
* Start attendance
* View attendance information
* Manage subject-wise attendance

### Teacher Workflow

```text
Teacher
   │
   ▼
Teacher Dashboard
   │
   ▼
Create Subject
   │
   ▼
Generate QR
   │
   ▼
Students Enroll
   │
   ▼
Start Attendance
   │
   ▼
Biometric Verification
   │
   ▼
Attendance Records
```

---

# 👨‍🎓 Student Module

The student module allows students to interact with subjects and biometric attendance.

### Student capabilities

* Access subject enrollment
* Scan QR code
* Join subjects
* Register biometric information
* Face-based identification
* Voice-based identification
* View attendance information

### Student Workflow

```text
Student
   │
   ▼
Scan QR / Open URL
   │
   ▼
Subject Enrollment
   │
   ▼
Biometric Registration
   │
   ├─────────────┐
   ▼             ▼
  Face          Voice
   │             │
   └──────┬──────┘
          ▼
      Attendance
```

---

# 📝 Attendance Workflow

The attendance process connects the recognition system with the database.

```text
Start Attendance
       │
       ▼
Student Provides
Face / Voice Input
       │
       ▼
Preprocessing
       │
       ▼
Embedding Generation
       │
       ▼
SVM Prediction
       │
       ▼
Student Identified
       │
       ▼
Check Subject Enrollment
       │
       ▼
Validate Attendance
       │
       ▼
Store Attendance
       │
       ▼
Supabase
```

The system can associate attendance with the appropriate:

* Student
* Subject
* Attendance session
* Date/time

---

# 🗄️ Database Architecture

SnapClass uses **Supabase**, backed by **PostgreSQL**, for application data storage.

The database is responsible for maintaining relationships between teachers, students, subjects, enrollments, and attendance records.

A simplified representation is:

```text
             TEACHER
                │
                │ creates
                ▼
             SUBJECT
                │
                │ enrollment
                ▼
        SUBJECT_STUDENTS
             /       \
            /         \
           ▼           ▼
       STUDENT     SUBJECT
           │
           │ attendance
           ▼
    ATTENDANCE_LOGS
```

### Main data concepts

#### Students

Stores information associated with registered students.

#### Teachers

Stores teacher-related information.

#### Subjects

Represents individual classes or subjects.

#### Subject Students

Maintains the relationship between students and the subjects they have joined.

#### Attendance Logs

Stores attendance records associated with students and subjects.

---

# 🛠️ Technology Stack

| Technology       | Role                            |
| ---------------- | ------------------------------- |
| **Python**       | Core application logic          |
| **Streamlit**    | Web application interface       |
| **Dlib**         | Face processing                 |
| **Librosa**      | Audio processing                |
| **Resemblyzer**  | Speaker embedding               |
| **SVM**          | Machine learning classification |
| **NumPy**        | Numerical processing            |
| **PIL**          | Image processing                |
| **Supabase**     | Backend platform                |
| **PostgreSQL**   | Relational database             |
| **QR Code**      | Subject enrollment              |
| **Git / GitHub** | Version control                 |

---

# 🏗️ Project Structure

The project is organized into application modules to separate the user interface, recognition pipelines, database operations, and reusable components.

```text
SnapClass/
│
├── app.py
│
├── src/
│   │
│   ├── components/
│   │   ├── header.py
│   │   ├── footer.py
│   │   └── ...
│   │
│   ├── ui/
│   │   ├── style_base_layout.py
│   │   └── ...
│   │
│   ├── face/
│   │   └── ...
│   │
│   ├── voice/
│   │   └── ...
│   │
│   ├── ml/
│   │   └── ...
│   │
│   ├── database/
│   │   └── ...
│   │
│   └── ...
│
├── .streamlit/
│   └── secrets.toml
│
├── requirement.txt
│
├── .gitignore
│
└── README.md
```

> The internal module structure may continue to evolve as SnapClass develops.

---

# ⚙️ Installation

## 1. Clone the repository

```bash
git clone https://github.com/anusharajanna027-git-in/SnapClass.git
```

```bash
cd SnapClass
```

---

## 2. Create a Virtual Environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### macOS / Linux

```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirement.txt
```

---

# 🔐 Configuration

SnapClass requires configuration values for external services such as Supabase.

Create the following file:

```text
.streamlit/secrets.toml
```

Example:

```toml
SUPABASE_URL = "your_supabase_url"
SUPABASE_KEY = "your_supabase_key"
```

Replace the placeholder values with your actual Supabase project credentials.

### ⚠️ Important

Never commit sensitive credentials to GitHub.

The following should remain private:

```text
.streamlit/secrets.toml
.env
API keys
Database passwords
Private credentials
```

Make sure sensitive files are included in `.gitignore`.

---

# ▶️ Running SnapClass

Activate your virtual environment first.

Then run:

```bash
streamlit run app.py
```

The application will start using Streamlit and can be accessed through the local browser URL provided by Streamlit.

---

# 🔄 Complete System Architecture

The complete SnapClass ecosystem can be represented as:

```text
                         SNAPCLASS
                            │
             ┌──────────────┴──────────────┐
             │                             │
          TEACHER                       STUDENT
             │                             │
             ▼                             ▼
       Teacher Dashboard            Student Interface
             │                             │
             ▼                             ▼
       Create Subject                Scan QR / URL
             │                             │
             ▼                             ▼
        Generate QR                  Join Subject
             │                             │
             └──────────────┬──────────────┘
                            │
                            ▼
                    Subject Enrollment
                            │
                            ▼
                    Biometric Registration
                            │
                 ┌──────────┴──────────┐
                 │                     │
                 ▼                     ▼
              FACE                   VOICE
                 │                     │
                Dlib               Librosa
                 │                     │
                 ▼                Resemblyzer
           Face Embedding        Voice Embedding
                 │                     │
                 └──────────┬──────────┘
                            │
                            ▼
                       SVM CLASSIFIER
                            │
                            ▼
                    Student Identity
                            │
                            ▼
                    Attendance Validation
                            │
                            ▼
                         Supabase
                            │
                            ▼
                    Attendance Records
```

---

# 🔒 Security Considerations

SnapClass handles biometric-related information and therefore requires careful security practices.

Recommended practices include:

* 🔐 Keep database credentials private
* 🔑 Store secrets outside source code
* 🚫 Never upload `secrets.toml`
* 🚫 Never upload `.env` files containing credentials
* 🛡️ Validate authenticated users
* 🛡️ Validate subject enrollment before attendance
* 🛡️ Prevent unauthorized database operations
* 📝 Validate biometric recognition before recording attendance
* 🔄 Prevent duplicate attendance records

---

# 📈 Advantages

## Compared with Manual Attendance

| Traditional Attendance    | SnapClass                                   |
| ------------------------- | ------------------------------------------- |
| Manual roll call          | AI-based identification                     |
| Time consuming            | Faster attendance process                   |
| Paper/manual records      | Digital database                            |
| Proxy attendance possible | Biometric verification                      |
| Manual subject enrollment | QR-based enrollment                         |
| Difficult to scale        | Designed for scalable software architecture |
| Manual record maintenance | Centralized database                        |

---

# 🌟 Why SnapClass?

SnapClass brings several technologies together into a single attendance platform:

```text
Artificial Intelligence
        +
Computer Vision
        +
Audio Processing
        +
Machine Learning
        +
Web Application
        +
Cloud Database
        =
      SNAPCLASS
```

The project demonstrates how modern AI technologies can be integrated into a practical educational software system.

---

# 🚀 Future Enhancements

Possible future improvements include:

### 📊 Advanced Analytics

* Attendance percentage dashboards
* Student performance analytics
* Subject-wise attendance statistics
* Monthly and semester reports

### 📱 Mobile Application

Development of dedicated Android and iOS applications.

### ☁️ Cloud Deployment

Deploy SnapClass to a production cloud environment for institution-wide usage.

### 🔔 Notifications

Automatic notifications for:

* Low attendance
* Absence
* Attendance confirmation
* Important classroom events

### 📄 Report Generation

Support for exporting attendance reports in:

* PDF
* Excel
* CSV

### 🔐 Enhanced Authentication

Implementation of stronger role-based authentication and authorization.

### 🧠 Model Improvements

Future versions can improve recognition robustness through:

* Larger datasets
* Better training strategies
* Improved preprocessing
* Threshold optimization
* Model evaluation
* Additional anti-spoofing techniques

### 🏫 Institutional Management

Future versions could support:

* Multiple institutions
* Departments
* Multiple teachers
* Multiple classrooms
* Academic years
* Semesters
* Course management

---

# 📊 Project Status

🚧 **Active Development**

SnapClass is currently under active development.

The project includes the core concepts required for:

* Face recognition
* Voice recognition
* Biometric feature extraction
* SVM-based classification
* Subject management
* QR-based enrollment
* Student enrollment
* Teacher workflows
* Attendance management
* Supabase database integration
* Streamlit user interface

Additional improvements and production-level refinements are continuously being developed.

---

# 🎯 Project Objective

The primary objective of SnapClass is to develop a **smart, automated, and secure attendance management system** that reduces the limitations of traditional attendance methods.

The project focuses on integrating:

> **Computer Vision + Speech Processing + Machine Learning + Web Technology + Cloud Database**

into a unified educational software platform.

---

# 👩‍💻 Author

## Anusha R

**SnapClass — AI-Powered Face & Voice Attendance Management System**

Developed as an AI/ML-based software project focused on intelligent classroom attendance automation.

---

# 📄 License

This project is currently intended for educational and development purposes.

A formal open-source license can be added when the project is prepared for public distribution.

---

# ⭐ SnapClass

> **Making attendance smarter with AI.**

If you find this project interesting, consider ⭐ starring the repository and following its development.

**© 2026 SnapClass**
