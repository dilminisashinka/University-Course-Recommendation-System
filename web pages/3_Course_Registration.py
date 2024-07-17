import streamlit as st
import pandas as pd
import mysql.connector
import sklearn
from sklearn.metrics.pairwise import cosine_similarity
import base64

st.set_page_config(layout="wide")

def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
     background-image: url("data:image/png;base64,%s");
     background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

set_background('uopSci.jpg')
st.markdown("# Course Registration ")

def connect_to_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="new",
            database="recommendations"
        )
        return conn

    except mysql.connector.Error as e:
        st.error(f"Error connecting to MySQL database: {e}")
        return None

def get_last_login_username():
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT RegNo FROM login_data ORDER BY login_time DESC LIMIT 1")
            last_username = cursor.fetchone()[0]
            return last_username
        except mysql.connector.Error as e:
            st.error(f"Error retrieving last login username: {e}")
        finally:
            cursor.close()
            conn.close()

student_id = get_last_login_username()
#st.write(student_id)

year = st.selectbox('Year :', (1, 2, 3, 4))

semester = st.selectbox('Semester :', ('I', 'II'))

if year == 2:            # and semester == 'I'
    subject = ('BL', 'BT', 'CH', 'CS', 'EN', 'MB', 'MT', 'SE', 'ZL', 'BMS', 'FS', 'PH', 'HR', 'MG',
                'GL', 'ES', 'MIC', 'EC', 'ST', 'BC', 'DSC', 'FNA', 'SCI', 'AS', 'SI', 'FND','None')
    droped_subject = st.selectbox('Dropped Subjects:', subject)
elif year == 3:                 # and semester == 'I'
    # Add subjects for year 3 semester I
    subjects = ("General (B.Sc.)","Biology", "Botany", "Chemistry","Enviornmental Science"," Computer Science",
                "Molecular Biology and Biotechnology", "Zoology","Physics", "Geology","Statistics",
                "Mathematics","Data Science","Micro Biology","Computation and Management (CM)",'Statisticals and Operation Research (SOR)')  # Add your subjects here
    degree = st.selectbox('Select Degree Programme:', subjects)

submit = st.button("Submit",type="primary")



conn = connect_to_db()
if conn:
    # Fetch data from the database
    query1 = "SELECT * FROM student_courses"
    student_courses = pd.read_sql(query1, conn)
    student_courses['RegNo'] = student_courses['RegNo'].fillna('').astype(str)  # Handle missing values and convert to string
    # query2 = "SELECT * FROM signUp_data"
    # signUp_data = pd.read_sql(query2,conn)
    conn.close()

# student_id = "s191001"

def recommend(student_id, year, semester, students_data, user_to_user_similarity_matrix):
    num_similar_students = 11
    # Assuming you have user_to_user_similarity_matrix available here

    # Step 1: Identify similar students for a particular student
    similar_students = user_to_user_similarity_matrix.loc[student_id].sort_values(ascending=False)[1:num_similar_students + 1].index

    # Step 2: Get unique courses for the specific year and semester for similar students
    courses_for_year_semester = students_data[
        (students_data['RegNo'].isin(similar_students)) & (students_data['year'] == year) & (
                    students_data['semester'] == semester)]['courseCode'].unique()

    # Step 3: Check if the student has taken the prerequisite courses for the recommended courses
    student_courses = students_data[students_data['RegNo'] == student_id]['courseCode'].unique()
    recommended_courses = []

    for course in courses_for_year_semester:
        prerequisites = students_data.loc[students_data['courseCode'] == course, 'Pre_requisites'].iloc[0]
        if pd.isnull(prerequisites) or prerequisites == 'NoPrerequisites':
            recommended_courses.append(course)
        else:
            prerequisites = [p.strip() for p in prerequisites.split(',')]  # Split prerequisites into a list and remove leading/trailing whitespaces
            if all(p in student_courses for p in prerequisites):
                recommended_courses.append(course)

    return recommended_courses

def recommend_courses():
    filtered_courses = student_courses[(student_courses['RegNo'] == student_id) & (student_courses['created_at'] <= '2024-02-23 11:49:19')]
    if not filtered_courses.empty:	    
        student_data = student_courses[student_courses['created_at'] <= '2024-02-23 11:49:19']
        studentID_Item_matrix = student_data.pivot_table(
            index='RegNo',
            columns=['Combination','courseCode','year'],
            aggfunc=lambda x: 1 if len(x) > 0 else 0, fill_value=0
        )

        user_to_user_similarity_matrix = pd.DataFrame(
            cosine_similarity(studentID_Item_matrix)
        )
        user_to_user_similarity_matrix.columns = studentID_Item_matrix.index
        user_to_user_similarity_matrix['RegNo'] = studentID_Item_matrix.index
        user_to_user_similarity_matrix = user_to_user_similarity_matrix.set_index('RegNo')
        recommended_courses = recommend(student_id, year, semester,student_data,user_to_user_similarity_matrix)
        return recommended_courses
    else:	   
        studentID_Item_matrix = student_courses.pivot_table(
            index='RegNo',
            columns=['Combination'],
            aggfunc=lambda x: 1 if len(x) > 0 else 0, fill_value=0
        )

        user_to_user_similarity_matrix = pd.DataFrame(
            cosine_similarity(studentID_Item_matrix)
        )
        user_to_user_similarity_matrix.columns = studentID_Item_matrix.index
        user_to_user_similarity_matrix['RegNo'] = studentID_Item_matrix.index
        user_to_user_similarity_matrix = user_to_user_similarity_matrix.set_index('RegNo')
        recommended_courses = recommend(student_id, year, semester,student_courses,user_to_user_similarity_matrix)
        return recommended_courses



# def filter_courses(student_id, year, semester, students_data,recommended_courses):
#     # Call the recommend function to get recommended courses
#     #recommended_courses = recommend(student_id, year, semester, students_data, user_to_user_similarity_matrix, num_similar_students)

#     # Get student's combination
#     student_combination = str(students_data.loc[students_data['RegNo'] == student_id, 'Combination'].iloc[0])
#     degree = students_data.loc[students_data['RegNo'] == student_id, 'degree'].iloc[0]
#     # Get student's year
#     student_year = students_data.loc[students_data['RegNo'] == student_id, 'year'].iloc[0]

#     compulsory_courses = []
#     supplementary_courses = []


#     for course in recommended_courses:
#         compulsory_for = students_data.loc[students_data['courseCode'] == course, 'Compulsory_for'].iloc[0]
#         if isinstance(compulsory_for, float):  # Check if it's a float (NaN)
#             compulsory_for = ''  # Replace NaN with empty string
#         else:
#             compulsory_for = [p.strip() for p in compulsory_for.split(',')]

#         if (year in [1, 2]) or (student_year==3 and degree=='General'):
#             if student_combination in compulsory_for:
#                 compulsory_courses.append(course)
#             else:
#                 supplementary_courses.append(course)
#         else:
#             if degree in compulsory_for :
#                 compulsory_courses.append(course)
#             else:
#                 supplementary_courses.append(course)

#     return compulsory_courses, supplementary_courses

# compulsory,supplimentary = filter_courses(student_id, year, semester, student_courses,recommend_courses())





def filter_courses(student_id, year, semester, students_data):
    # Call the recommend function to get recommended courses
    #recommended_courses = recommend(student_id, year, semester, students_data, user_to_user_similarity_matrix, num_similar_students)
    recommended_courses = recommend_courses()
    Foundation_courses = ['EN100','CS100','MT100','BL100','MT120','FND114']
    # Get student's combination
    student_combination = str(students_data.loc[students_data['RegNo'] == student_id, 'Combination'].iloc[0])
    
    degree = students_data.loc[students_data['RegNo'] == student_id, 'degree'].iloc[0]
    # Get student's year
    

    compulsory_courses = []
    supplementary_courses = []

    
    # if year==2 and semester=='I':
    #    droped_subject= input('Enter the droped subject:') 

    
    # if year==3 and semester=='I':
    #   degree= input('Enter Your Degree Progeam:')
    
    for course in recommended_courses:
        #subject= students_data.loc[students_data['courseCode'] == course, 'subject'].iloc[0]
        compulsory_for = students_data.loc[students_data['courseCode'] == course, 'Compulsory_for'].iloc[0]
        if isinstance(compulsory_for, float):  # Check if it's a float (NaN)
            compulsory_for = ''  # Replace NaN with empty string
        else:
            compulsory_for = [p.strip() for p in compulsory_for.split(',')]
       
        if year == 1 and semester == 'I':
            if student_combination in compulsory_for:
                compulsory_courses.append(course)
            else:
                if course in Foundation_courses:
                  compulsory_courses.append(course)
                else:
                  supplementary_courses.append(course)
        elif (year == 1 and semester == 'II') or (year==2 and semester=='II') or (year==3 and degree=='General (B.Sc.)'):
            if student_combination in compulsory_for:
                compulsory_courses.append(course)
            else:
                supplementary_courses.append(course)
        elif year==2 and semester=='I':
            subject= students_data.loc[students_data['courseCode'] == course, 'subject'].iloc[0]
            if student_combination in compulsory_for:
                
                if subject == droped_subject:
                  supplementary_courses.append(course)
                else:
                  compulsory_courses.append(course)
            else:
                supplementary_courses.append(course)
        else:
            if degree in compulsory_for :
                compulsory_courses.append(course)
            else:
                supplementary_courses.append(course)

    return compulsory_courses, supplementary_courses

# student_id = 's181504'
# year = 4
# semester = 'I'
# num_similar_students = 11
# compulsory_courses, supplementary_courses = filter_courses(student_id, year, semester, students_courses, user_to_user_similarity_matrix, num_similar_students)
# print("Compulsory courses:", compulsory_courses)
# print("Supplementary courses:", supplementary_courses)

compulsory, supplementary = filter_courses(student_id, year, semester, student_courses)




if submit:
    recommended_courses = recommend_courses()
    st.markdown("## Recommended For You")
    col1, col2= st.columns(2)
    with col1:
        # if all(course in recommended_courses for course in compulsory):
        st.markdown("### Compulsory Courses : ")
        for course in compulsory:
            # Find the row corresponding to the current course code
            course_row = student_courses[student_courses['courseCode'] == course]
            if not course_row.empty:
                credit = course_row['credits'].iloc[0]  # Assuming 'credit' is the column containing credits
                courseName = course_row['courseName'].iloc[0]
                st.markdown(f'<div style="background-color: {"#043583"}; color: {"white"}; padding: 10px; border-radius: 5px; margin-bottom: 10px;">{course} [{courseName}] - Credits : {credit} </div>', unsafe_allow_html=True)
            else:
                st.error(f'No data found for course: {course}')
    
                
             
    with col2:
        st.markdown("### Supplimentary Courses : ")
        for course in supplementary:
            # Find the row corresponding to the current course code
            course_row = student_courses[student_courses['courseCode'] == course]
            if not course_row.empty:
                credit = course_row['credits'].iloc[0]  # Assuming 'credit' is the column containing credits
                courseName = course_row['courseName'].iloc[0]
                st.markdown(f'<div style="background-color: {"#043583"};  color: {"white"};padding: 10px; border-radius: 5px; margin-bottom: 10px;">{course} [{courseName}] - Credits : {credit} </div>', unsafe_allow_html=True)
            else:
                st.error(f'No data found for course: {course}')
        
