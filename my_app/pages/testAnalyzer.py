from google import genai
import streamlit as sd
import streamlit as st
from PIL import Image
#import pymongo
from pymongo import MongoClient
import os

sd.title("Test Analysis")

if __name__ == '__main__':
    client = genai.Client(api_key=os.getenv("API_KEY"))
    mclient = MongoClient(os.getenv("MONGO_URI"))
    db = mclient["user_info"]
    collection = db["diagnostics"]

    questions = []
    user_id = st.session_state.get("user_name")
    # Based on a random collection from MongoDB
    allResults = list(collection.find({"user_name": user_id}))
    sampleResults = allResults[0]

    #print("Test : Client Data \n" + str(sampleResults))

    sd.subheader("Cognitive Analysis Test:")
    # Cognitive Assessment Analysis
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents="Briefly define what MMSE and SAGE (Self-Administered Gerocognitive Examination) tests are"
    )
    questions.append(response.text)
    sd.write(response.text)

    #Question Section
    #Dictionary parsing test
    sd.write("Question One Results:")
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents="These next two entries are from the MMSE test. Are they similar to today's date which is April 19, 2025?:" + str(sampleResults["memory_test_m"]) + " " + str(sampleResults["memory_test_d"]) + "."
    )
    questions.append(response.text)
    sd.write(response.text)

    sd.write("Question 2a:")
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents="Is this an accurate similarity for watches and rulers? " + str(sampleResults["similarity_qs"]) + "."
    )
    questions.append(response.text)
    sd.write(response.text)

    sd.write("Question 2b:")
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents="Is this a good response for the number of nickels in 60 cents:" + str(sampleResults["similarity_qs_2"]) + "?"
    )
    questions.append(response.text)
    sd.write(response.text)

    sd.write("Question 2c:")
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents="Is this a good response for the number of nickels in 60 cents:" + str(sampleResults["similarity_qs_2"]) + "?"
    )
    questions.append(response.text)
    sd.write(response.text)

    sd.write("Question 3:")
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents="Is this the same as $6.55:" + str(sampleResults["similarity_qs_3"]) + "?"
    )
    questions.append(response.text)
    sd.write(response.text)

    sd.write("Question 4:")
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents="Given the list " + str(sampleResults["animal_names"]) + ", how many are considered animals? How would you describe the other input? State this in a positive way"
    )
    questions.append(response.text)
    sd.write(response.text)

    sd.write("Question 5:")
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents="Did the user write i am done: " + str(sampleResults["similarity_qs_3"]) + "?"
    )
    questions.append(response.text)
    sd.write(response.text)

    sd.write("Final Score:")
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents = "Given the following input: " + str(questions) + "As a number value only, rate the user's performance on a scale of 0 to 30"
    )
    score = response.text
    sd.write(score)


    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents = "In two words, based on the score " + score + " of 30 given, state whether the user is either Cognitively Impaired or Cognitively Sound"
    )
    mode = response.text
    sd.write(mode)

if st.button("Go to Game Hub for cognitively impaired"):
            st.markdown("""
                <meta http-equiv="refresh" content="2;url=/m_impaired" />
            """, unsafe_allow_html=True)

if st.button("Go to Game Hub for cognitively normal"):
            st.markdown("""
                <meta http-equiv="refresh" content="2;url=/m_normal" />
            """, unsafe_allow_html=True)




