import pymongo
import certifi
import streamlit as st
import datetime
from PIL import Image
import os


st.title('Welcome to your Personalized Alzheimer Care Center!')

st.write("Please answer the following questions to help us to customize best treatment for you:")
#  MongoDB connection string
uri = os.getenv("MONGO_URI")

# Create MongoClient with the certifi certificates
client = pymongo.MongoClient(uri, tlsCAFile=certifi.where())

# Example usage: Access the database and collection
db = client["store"]
collection = db["products"]
user_auth = "38373892374"  # Example user ID

# Test questions
name = st.text_input("Name:")
dob = st.date_input("Date of Birth:")
school_level = st.text_input("How far did you get in school?")
gender = st.radio("I am a", options=["", "Man", "Woman", "Other"], index=0)
ethnicity = st.radio("Ethnicity:", ["", "Asian", "Black", "Hispanic", "White", "Other"], index=0)
memory_issues = st.radio("Have you had any problems with memory or thinking?", ["","Yes", "Only Occasionally", "No"], index=0)
family_memory_problems = st.radio("Have you had any blood relatives that have had problems with memory or thinking?", ["","Yes", "No"], index=0)
balance_problems = st.radio("Do you have balance problems?", ["","Yes", "No"], index=0)

if balance_problems == "Yes":
    balance_cause = st.text_input("If yes, do you know the cause? (Specify reason):")
    
stroke_history = st.radio("Have you ever had a major stroke?", ["", "Yes", "No"],index=0)
mini_stroke = st.radio("A minor or mini-stroke?", ["","Yes", "No"],index=0)
depression = st.radio("Do you currently feel sad or depressed?", ["","Yes", "Only Occasionally", "No"],index=0)
personality_change = st.radio("Have you had any change in your personality?", ["","Yes", "No"],index=0)
if personality_change == "Yes":
    personality_changes = st.text_input("If yes, specify changes:")

everyday_difficulties = st.radio("Do you have more difficulties doing everyday activities due to thinking problems?", ["","Yes", "No"],index=0)

# Memory Test Question
memory_test_month = st.text_input("What is today’s date? (from memory – no cheating!) Month:")
memory_test_date = st.text_input("Date:")
memory_test_year = st.text_input("Year:")

# Get current date
current_date = datetime.date.today()
current_month = current_date.month
current_day = current_date.day
current_year = current_date.year

if os.path.exists("test_image_1.png"):
    image = Image.open("test_image_1.png")
    st.image(image, use_column_width=True)

image = st.text_input("Please name the image")

# when user clicks on submit, save database in MongoDB
if st.button('Submit'):
    if not name:
        st.warning("Please enter your name.")
    else:
        form_data = {
            "user_auth": user_auth,
            "user_id": name.lower().replace(" ", "_"), 
            "name": name,
            "date_of_birth": str(dob),
            "education_level": school_level,
            "gender": gender,
            "ethnicity": ethnicity,
            "memory_problems": memory_issues,
            "family_history": family_memory_problems,
            "balance_problems": balance_problems,
            "stroke_history": {
                "yes": mini_stroke,
            },
            "depression": depression,
            "test_date_guess": {
                "month": current_month,
                "day": current_day,
                "year": current_year
            },
            "submission_time": datetime.datetime.now()  # Added timestamp for tracking
        }

        # Insert the new record in MongoDB
        collection.insert_one(form_data)

        st.success("Form submitted and saved to MongoDB!")

if st.button("View Data"):
    os.system("streamlit run vers.py")