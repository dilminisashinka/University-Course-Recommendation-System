# University Course Recommendation System

This application serves as a course recommender system based on collaborative filtering. It recommends courses to users by finding similar profiles, using the Streamlit framework to create a user-friendly web service.

## Features

- **Collaborative Filtering**: This recommender system uses cosine similarity calculated from a user-item matrix to recommend courses. Based on the similarity between users, the system recommends courses from the most similar profiles of past students.
- **SQL Integration**: User data, course information, and course registration data are stored in MySQL.

## Tech Used
- **Language**: Python
- **Web Framework**: Streamlit
- **Database**: MySQL
- **Algorithm**: Collaborative Filtering
- **Configuration**: `config.toml`, `secrets.toml`

## Usage

Follow these instructions to set up and run the course recommendation system on your local system:

1. **Clone the Repository**:

   ```sh
   git clone https://github.com/your-username/course-recommendation-system.git
   cd course-recommendation-system

2. **Create a Virtual Environment**:
```python -m venv venv```
```source venv/bin/activate``` ` # On Windows, use ```venv\Scripts\activate```


3. **Install the Required Python Packages**:
`pip install -r requirements.txt`

4. **Set Up the MySQL Database**:
- Create a MySQL database.
- Create the necessary tables.
- Update the config.toml and secrets.toml files with database connection details.

5. **Create and Configure the config.toml File**:
[connections.mysql]
```
dialect = "mysql"
host = "localhost"
port = 3306
database = "recommendations"
username = "root"
password = ""
```

6. **Create and Configure the secrets.toml File**:
[mysql]
```
host = "localhost"
port = 3306
database = "recommendations"
user = "root"
password = "your_password_here"
```
 
7. **Run the Streamlit Application**:
```
streamlit run recommender.py
```

8. **Access the Application**:
Open your web browser and go to http://localhost:8501.
