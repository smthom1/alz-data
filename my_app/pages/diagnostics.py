import pymongo
import certifi
import streamlit as st
import datetime
from PIL import Image
import os

# To Do:
# Sending date what sophia has said
# clean the date of birth question
# 
if not st.session_state.get("intake_complete", False):
    st.warning("Please complete the intake form first.")
    st.stop()
st.title('Welcome to your Personalized Alzheimer Care Center!')

st.write("Please answer the following questions to help us to customize best treatment for you:")
#  MongoDB connection string
uri = ""

# Create MongoClient with the certifi certificates
client = pymongo.MongoClient(uri, tlsCAFile=certifi.where())

# Example usage: Access the database and collection
db = client["user_info"]
collection = db["diagnostics"]

# Fetch all records for the given auth_user

user_id= "sample_user"  # Replace with actual user ID
data = list(collection.find({"user_id": user_id}))
print(data)

# Memory Test Question

#Test Qs 1:
memory_test_month = st.text_input("What is today’s date? (from memory – no cheating!) Month:")
memory_test_date = st.text_input("Date:")
memory_test_year = st.text_input("Year:")

# Get current date
current_date = datetime.date.today()
# make sure that gets send out to database, done
current_month = current_date.month
current_day = current_date.day
current_year = current_date.year

#Test Qs 2:
image_1_name = ""
if os.path.exists("test_image_1.png"):
    image_1 = Image.open("test_image_1.png")
    st.image(image_1, use_column_width=True)
    image_1_name = st.text_input("Please name the first image")

# Test Qs 3:
image_2_name = ""
if os.path.exists("test_image_2.png"):
    image_2 = Image.open("test_image_2.png")
    st.image(image_2, use_column_width=True)

    image_2_name = st.text_input("Please name the second image")

# Test Qs 4,5,6:
similarity_qs_1 = st.text_input("How are a watch and a ruler similar? Write down how they are alike. They both are... what?")
similarity_qs_2 = st.text_input("How many nickels are in 60 cents?")
similarity_qs_3 = st.text_input("You are buying 13.45 dollar of groceries.How much change would you receive back from a 20 dollar bill")

# Test Qs 4:
mem_qs_end = st.write("Do later only after completing this entire test: At the bottom of the very last page: Write “I am done” on the blank line provided")

# Test Qs 5:
animal_names = st.write("Write down the names of 12 different animals (don’t worry about spelling):")
animal_names = []

for i in range(1, 13):
    name = st.text_input(f"Animal {i}:", key=f"animal_{i}")
    animal_names.append(name)

# Test Qs 6:
image_3_name = ""
if os.path.exists("test_image_3.png"):
    image_3 = Image.open("test_image_3.png")
    st.image(image_3, use_column_width=True)
    image_3_name = st.write("Please take a look at the image.")
sequence_qs_1 = st.markdown("Select the correct alternating sequence starting from 1:")

sequence = [
    st.selectbox("Step 1", ["", "1", "A", "2", "B", "3", "C"], key="q_1_step1"),
    st.selectbox("Step 2", ["", "1", "A", "2", "B", "3", "C"], key="q_1_step2"),
    st.selectbox("Step 3", ["", "1", "A", "2", "B", "3", "C"], key="q_1_step3"),
    st.selectbox("Step 4", ["", "1", "A", "2", "B", "3", "C"], key="q_1_step4"),
    st.selectbox("Step 5", ["", "1", "A", "2", "B", "3", "C"], key="q_1_step5"),
    st.selectbox("Step 6", ["", "1", "A", "2", "B", "3", "C"], key="q_1_step6")
]

correct_sequence = ["1", "A", "2", "B", "3", "C"]
if st.button("Check Answer"):
    if sequence == correct_sequence:
        st.success("Correct!")
    else:
        st.error("Remember to alternate numbers and letters, or you can skip to next question!")

# Test Qs 7:
image_4_name = ""
if os.path.exists("test_image_4.png"):
    image_4 = Image.open("test_image_4.png")
    st.image(image_4, use_column_width=True)
    image_4_name = st.write("Now, Please take a look at this second image.")

sequence_qs_2 = st.markdown("Select the correct sequence starting at 1 and alternating numbers and letters in order before ending at F (1 to A to 2 to B and so on)")
sequence_2 = [
    st.selectbox("Step 1", ["", "A", "B", "C", "D", "E", "F"], key="q_2_step1"),
    st.selectbox("Step 2", ["", "A", "B", "C", "D", "E", "F"], key="q_2_step2"),
    st.selectbox("Step 3", ["", "A", "B", "C", "D", "E", "F"], key="q_2_step3"),
    st.selectbox("Step 4", ["","A", "B", "C", "D", "E", "F"], key="q_2_step4"),
    st.selectbox("Step 5", ["","A", "B", "C", "D", "E", "F"], key="q_2_step5"),
    st.selectbox("Step 6", ["","A", "B", "C", "D", "E", "F"], key="q_2_step6")
]
correct_sequence_2 = ["A", "B", "C", "D", "E", "F"]
if st.button("Check  Answer"):
    if sequence_2 == correct_sequence_2:
        st.success("Correct!")
    else:
        st.error("Remember to alternate numbers and letters, or you can skip to next question!")

# Test Qs 8:
mem_qs_end= st.text_input("")

# when user clicks on submit,  # save database in MongoDB

sequence_answer_1 = "sequence"  # This should be the actual answer selected by the user
sequence_answer_2 = "sequence_2"  # Similarly, extract this from the user input
if st.button('Submit'):
    form_data = {
        "user_id": "sample_user", 
        "current_month": current_month,  
        "current_day": current_day,      
        "current_year": current_year,    
        "memory_test_m": memory_test_month,
        "memory_test_d": memory_test_date,
        "memory_test_d": memory_test_year,
        "image_1_answer": image_1_name,
        "image_2_answer": image_2_name,
        "similarity_qs": similarity_qs_1,
        "similarity_qs_2": similarity_qs_2,
        "similarity_qs_3": similarity_qs_3,
        "animal_names": animal_names,
        "sequence_answer":sequence_answer_1,
        "sequence_qs_2":sequence_answer_2,
        "last_qs": mem_qs_end,
    }

    collection.insert_one(form_data)
    st.success("Your answers has been succesfully submitted! Please move on to next page to see the results.")
    # create a button for "results button"

