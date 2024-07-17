import streamlit as st
import mysql.connector
import base64

st.set_page_config(layout="wide")    
#st.sidebar.image("uop.jpg", use_column_width=True)
st.markdown("# Login ")

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


#st.write("Welcome to the LMS Faculty of Science")
st.success("Please login with the username and password")

#username = st.text_input("Username (Username should be your registration number)")
#def username():
username = st.text_input("Username (Username should be your registration number)")
    #return username

password = st.text_input('Password', type='password')

signIn = st.button("Sign In",type="primary")

def connect_to_db():
    try:
        conn = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "new",
            database = "recommendations"
        )
        return conn
    except mysql.connector.Error as e:
        st.error(f"Error connecting to MySQL database: {e}")
        return None

def validate_user(username, password):
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        try:
            #cursor.execute("SELECT * FROM signUp_data WHERE regNo = %s", (username,))
            cursor.execute("SELECT RegNo,password FROM student_courses WHERE regNo = %s LIMIT 1", (username,))
            user_data = cursor.fetchone()
            if user_data:
                if user_data[1] == password:  # Assuming password is stored in the 5th column
                    cursor.execute("INSERT INTO login_data (RegNo, password, login_time) VALUES (%s, %s, NOW())", (username, password))
                    conn.commit()
                    return True
                else:
                    return False
            else:
                return False
        except mysql.connector.Error as e:
            st.error(f"Error validating user: {e}")
        finally:
            cursor.fetchall()
            cursor.close()
            conn.close()
    else:
        return False

if signIn:
    if username and password:
          if validate_user(username, password):
               st.success("Login successful!")
               st.link_button("Course Registration ➡️","http://localhost:8501/Course_Registration",type="primary")
            # Redirect user to Course Registration page
            # You can use Streamlit's 'st.experimental_set_query_params()' function for redirection
          else:
            st.error("Invalid username or password. Please try again.")
    else:
        st.warning("Please enter username and password.")
