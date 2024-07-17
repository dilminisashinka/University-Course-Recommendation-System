import streamlit as st
import mysql.connector 
import base64

st.set_page_config(page_title="Home", layout="wide")
st.sidebar.image("uopSci.jpg", use_column_width=True)

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

col1, col2, col3, col4, col5, col6, col7 ,col8, col9, col10, col11= st.columns(11)
with col10:
    st.link_button("Sing In", "http://localhost:8501/Login",type="primary")  # Use a specific key for the button
    

with col11:
    st.link_button("Sign Up","http://localhost:8501/Create_Account", type="primary")

st.write(
    """
    <h1 style='text-align: center;color: white; font-size: 60px'>Faculty of Science University of Peradeniya</h1>
    """,
    unsafe_allow_html=True)

