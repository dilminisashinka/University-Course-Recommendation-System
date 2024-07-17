import streamlit as st
import mysql.connector
import re
import base64

st.set_page_config(layout="wide")
st.markdown("# Create Account ")
st.write("Welcome to the LMS Faculty of Science")

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

set_background('back4.jpg')

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

def import_data():
    if signUp:
        # Add data to the database
        conn = connect_to_db()
        if conn:
            cursor = conn.cursor()
            try:
                #cursor.execute("INSERT INTO SignUp_data VALUES (%s, %s, %s, %s, %s)", (regNo, degreeType, combination, acedamic_year, password))
                cursor.execute("INSERT INTO student_courses (RegNo,Combination,password) VALUES (%s, %s,%s)", (regNo, combination,password))
                conn.commit()
                st.success("Your account has been successfully created.")
                st.markdown("[Go To Login](http://localhost:8501/Login)")
            except mysql.connector.Error as e:
                st.error(f"Error inserting data into database: {e}")
            finally:
                cursor.close()
                conn.close()

regNo_placeholder = st.empty()
regNo = st.text_input("Registration Number :")
degreeType = st.selectbox(
    'Degree Program :',
    ('Physical Science', 'Bio Science', 'Computation and Management (CM)', 'Statisticals and Operation Research (SOR)')
)
combination = st.selectbox("Subject Combination : ", ('1', '2', '3', '4', '8', '15', '18', '19', '21', '22', '26', '27', '28', '30', '31', '32', 'CM', 'SOR'))
acedamic_year = st.text_input("Academic Year (Ex: 2019/2020) :", max_chars=9, placeholder="YYYY/YYYY")
password = st.text_input('Password', type='password')
confirm_password = st.text_input('Confirm Password', type='password')
signUp = st.button("Sign Up", type="primary")

# Define a regular expression pattern to match the desired format of registration number
regNo_pattern = r'^s\d+$'

# Define a regular expression pattern to match the desired format of academic year
acedamic_year_pattern = r'^\d{4}/\d{4}$'

if regNo and degreeType and combination and acedamic_year and password and confirm_password:
    if re.match(regNo_pattern, regNo):  # Validate registration number format
        if re.match(acedamic_year_pattern, acedamic_year):  # Validate academic year format
            if password == confirm_password:
                import_data()
            else:
                st.warning("Passwords do not match")
        else:
            st.warning("Academic year should be in the format like '2019/2020'")
    else:
        regNo_placeholder.warning("Registration number should be in the format like 's181000'")
elif regNo:  # If regNo is filled but other fields are not, check its format
    if not re.match(regNo_pattern, regNo):
        regNo_placeholder.warning("Registration number should be in the format like 's181000'")
