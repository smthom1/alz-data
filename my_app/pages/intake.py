import pymongo
import certifi
import streamlit as st
import datetime
from PIL import Image
import os
from streamlit_extras.switch_page_button import switch_page

# To Do:
# Sending date what sophia has said
# clean the date of birth question
#
st.title('Welcome to your Personalized Alzheimer Care Center!')

st.write("Please answer the following questions to help us to customize best treatment for you:")
st.write("The following information is confidential and will not be shared with anyone.")
#  MongoDB connection string
uri = os.getenv("MONGO_URI")

# Create MongoClient with the certifi certificates
client = pymongo.MongoClient(uri, tlsCAFile=certifi.where())

db = client["user_info"]
collection = db["intake"]

# Intake questions
name = st.text_input("Name:")
dob = st.date_input("Date of Birth:", value=None)
school_level = st.text_input("How far did you get in school?")
gender = st.radio("I am a", options=["", "Man", "Woman", "Other"], index=0)
ethnicity = st.radio("Ethnicity:", ["", "Asian", "Black", "Hispanic", "White", "Other"], index=0)
memory_issues = st.radio("Have you had any problems with memory or thinking?", ["","Yes", "Only Occasionally", "No"], index=0)
family_memory_problems = st.radio("Have you had any blood relatives that have had problems with memory or thinking?", ["","Yes", "No"], index=0)

#balance_problems will hold yes or no
balance_problems = st.radio("Do you have balance problems?", ["","Yes", "No"], index=0)
balance_cause = "N/A"
#balance_cause will hold users answer
if balance_problems == "Yes":
    balance_cause = st.text_input("If yes, do you know the cause? (Specify reason):")
    
stroke_history = st.radio("Have you ever had a major stroke?", ["", "Yes", "No"],index=0)
mini_stroke = st.radio("A minor or mini-stroke?", ["","Yes", "No"],index=0)
depression = st.radio("Do you currently feel sad or depressed?", ["","Yes", "Only Occasionally", "No"],index=0)

#personality_change holds yes or no
personality_change = st.radio("Have you had any change in your personality?", ["","Yes", "No"],index=0)
personality_changes = "N/A"  # default value
#personality_changes holds the value (answer of the user)
if personality_change == "Yes":
    personality_changes = st.text_input("If yes, specify changes:")


everyday_difficulties = st.radio("Do you have more difficulties doing everyday activities due to thinking problems?", ["","Yes", "No"],index=0)


# when user clicks on submit,  # save database in MongoDB
if st.button('Submit'):
    if not name:
        st.warning("Please enter your name.")
    else:
        form_data = {
            "name": name,
            "date_of_birth": str(dob),
            "education_level": school_level,
            "gender": gender,
            "ethnicity": ethnicity,
            "memory_problems": memory_issues,
            "family_history": family_memory_problems,
            "balance_problems": balance_problems,
            "balance_cause": balance_cause if balance_problems == "Yes" else "N/A",
            "stroke_history": stroke_history,
            "mini_stroke": mini_stroke,
            "depression": depression,
            "personality_change": personality_change,
            "personality_changes": personality_changes if personality_change == "Yes" else "N/A",
            "activity_difficulty": everyday_difficulties,
        }
        collection.insert_one(form_data)
        st.session_state.intake_complete = True
        st.success("Your answer has been successfully submitted! Please move on to test questions.")
        
        #create a button for move on the next
        # if st.button("Move on to Test Questions"):
        #     st.switch_page("diagnostics.py") 