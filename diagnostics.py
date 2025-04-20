import pymongo
import certifi
import streamlit as st
import datetime
from PIL import Image
import os
import random

st.markdown("""
    <style>
        /* Hide sidebar */
        section[data-testid="stSidebar"] {
            display: none !important;
        }

        /* Hide the collapsed sidebar toggle (arrow button) */
        div[data-testid="collapsedControl"] {
            display: none !important;
        }

        /* Adjust the main block to take full width */
        div[class*="main"] {
            margin-left: 0 !important;
        }

        /* Hide top menu hamburger if visible */
        header {
            visibility: hidden;
        }
    </style>
""", unsafe_allow_html=True)

# To Do:
# Sending date what sophia has said
# clean the date of birth question
# 
# if not st.session_state.get("intake_complete", False):
#     st.warning("Please complete the intake form first.")
#     st.stop()
st.title('Welcome to your Personalized Alzheimer Care Center!')

st.write("Please answer the following questions to help us to customize best treatment for you:")
#  MongoDB connection string
uri = os.getenv("MONGO_URI")

# Create MongoClient with the certifi certificates
client = pymongo.MongoClient(uri, tlsCAFile=certifi.where())

# Example usage: Access the database and collection
db = client["user_info"]
collection = db["diagnostics"]

user_name = st.session_state.get("user_name")

# Fetch all records for the given auth_user

user_id= "sample_user"  # Replace with actual user ID
data = list(collection.find({"user_id": user_id}))

# Memory Test Question

# Test Qs 1: "What is today’s date? (from memory – no cheating!)"
memory_test_month = st.text_input("What is today’s date? (from memory – no cheating!) Month:")
memory_test_date = st.text_input("Date:")
memory_test_year = st.text_input("Year:")

# Get current date
current_date = datetime.date.today()
# make sure that gets send out to database, done
current_month = current_date.month
current_day = current_date.day
current_year = current_date.year

# Test Qs 2.1: "Name the following pictures (don’t worry about spelling):" wreath
image_1_name = ""
if os.path.exists("test_image_1.png"):
    image_1 = Image.open("test_image_1.png")
    st.image(image_1, use_column_width=True)
    image_1_name = st.text_input("Please name the first image")

# Test Qs 2.2: "Name the following pictures (don’t worry about spelling):" volcano
image_2_name = ""
if os.path.exists("test_image_2.png"):
    image_2 = Image.open("test_image_2.png")
    st.image(image_2, use_column_width=True)

    image_2_name = st.text_input("Please name the second image")

# Test Qs 3, 4, 5: "Answer these questions:" ...
similarity_qs_1 = st.text_input("How are a watch and a ruler similar? Write down how they are alike. They both are... what?")
similarity_qs_2 = st.text_input("How many nickels are in 60 cents?")
similarity_qs_3 = st.text_input("You are buying \$13.45 of groceries. How much change would you receive back from a 20 dollar bill")

# Test Qs 6:
mem_qs_end = st.write("After completing the test at the last question, type “I am done” on the blank line provided.")

# [Test Qs 7 and 8 are drawn - SKIPPED]

# Test Qs 9:
animal_names = st.write("Write down the names of 12 different animals (don’t worry about spelling):")
animal_names = []

for i in range(1, 13):
    name = st.text_input(f"Animal {i}:", key=f"animal_{i}")
    animal_names.append(name)

# Test Qs _: "Draw a line from one circle to another starting at 1 and alternating numbers and letters (1 to A to 2 to B to 3 to C)."
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

# Test Qs 7: "Do the following: Draw a line from one circle to another starting at 1 and alternating numbers and letters in order before ending at F (1 to A to 2 to B and so on)."
# image_4_name = ""
# if os.path.exists("test_image_4.png"):
#     image_4 = Image.open("test_image_4.png")
#     st.image(image_4, use_column_width=True)
#     image_4_name = st.write("Now, Please take a look at this second image.")

# sequence_qs_2 = st.markdown("Select the correct sequence starting at 1 and alternating numbers and letters in order before ending at F (1 to A to 2 to B and so on)")
# sequence_2 = [
#     st.selectbox("Step 1", ["", "A", "B", "C", "D", "E", "F"], key="q_2_step1"),
#     st.selectbox("Step 2", ["", "A", "B", "C", "D", "E", "F"], key="q_2_step2"),
#     st.selectbox("Step 3", ["", "A", "B", "C", "D", "E", "F"], key="q_2_step3"),
#     st.selectbox("Step 4", ["","A", "B", "C", "D", "E", "F"], key="q_2_step4"),
#     st.selectbox("Step 5", ["","A", "B", "C", "D", "E", "F"], key="q_2_step5"),
#     st.selectbox("Step 6", ["","A", "B", "C", "D", "E", "F"], key="q_2_step6")
# ]
# correct_sequence_2 = ["A", "B", "C", "D", "E", "F"]
# if st.button("Check  Answer"):
#     if sequence_2 == correct_sequence_2:
#         st.success("Correct!")
#     else:
#         st.error("Remember to alternate numbers and letters, or you can skip to next question!")

# Initialize characters and grid
characters = ['A', 'B', 'C', 'D', 'E', '1', '2', '3', '4', '5']
grid_size = 5  # 5x2 grid

# Randomize character positions on first load
if "shuffled" not in st.session_state:
    st.session_state.shuffled = random.sample(characters, len(characters))

# Store selected tiles
if "selection" not in st.session_state:
    st.session_state.selection = []

# Store formed pairs
if "pairs" not in st.session_state:
    st.session_state.pairs = []

st.markdown("Select the correct alternating sequence starting from 1: (1 → A, 2 → B, ...)")

# Display the grid
cols = st.columns(5)
for i, char in enumerate(st.session_state.shuffled):
    col = cols[i % 5]
    with col:
        if st.button(char, key=f"btn_{i}"):
            if len(st.session_state.selection) < 2:
                st.session_state.selection.append(char)

# Show pair if two tiles are selected
if len(st.session_state.selection) == 2:
    pair = tuple(st.session_state.selection)  # Keep them in the order user selected
    st.session_state.pairs.append(pair)  # Store the pair
    st.session_state.selection = []  # Clear selection for the next round
    
# Add a reset button
if st.button("Reset"):
    st.session_state.shuffled = random.sample(characters, len(characters))
    st.session_state.selection = []
    st.session_state.pairs = []
    st.rerun()

# Display all formed pairs
if st.session_state.pairs:
    st.subheader("Formed Pairs:")
    for idx, (a, b) in enumerate(st.session_state.pairs):
        st.write(f"{idx+1}. {a} - {b}")

# Test Qs 8:
mem_qs_end= st.text_input("")

# when user clicks on submit,  # save database in MongoDB

sequence_answer_1 = "sequence"  # This should be the actual answer selected by the user
sequence_answer_2 = "sequence_2"  # Similarly, extract this from the user input
if st.button('Submit and see results'):
    form_data = {
        "user_name": user_name,
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
        # "sequence_qs_2":sequence_answer_2,
        "formed_pairs": st.session_state.pairs,
        "last_qs": mem_qs_end,
    }

    collection.insert_one(form_data)
    st.success("Your answers has been succesfully submitted! Please move on to next page to see the results.")
    st.session_state["form_data"] = form_data

    st.markdown("""
            <meta http-equiv="refresh" content="2;url=/data_view" />
        """, unsafe_allow_html=True)