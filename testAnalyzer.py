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
        model="gemini-2.0-flash", contents="The User had taken a test similar to the MMSE and SAGE (Self-Administered Gerocognitive Examination) tests. Give a brief introduction to what the given test is"
    )
    sd.write(response.text)

    #Question Section
    #Dictionary parsing test
    sd.write("Question One Results:")
    questionDivider = client.chats.create(model='gemini-2.0-flash')
    q = questionDivider.send_message(
        message="These next two entries are from the MMSE test. Are they similar to today's date which is April 19, 2025?:" + sampleResults["memory_test_m"] + " " + sampleResults["memory_test_d"] + "."
    )
    questions.append(q.text)
    sd.caption(q.text)

    # sd.write("Question 2a Results:")
    # q = client.models.generate_content(
    #     model='gemini-2.0-flash',
    #     contents=[
    #         'Is the object in the image similar to a ' + str(sampleResults["image_1_answer"]) + '?',
    #         Image.open("Wreathe.png")
    #     ]
    # )
    # questions.append(q.text)
    # sd.caption(q.text)

    # sd.write("Question 2b Results:")
    # q = client.models.generate_content(
    #     model='gemini-2.0-flash',
    #     contents=[
    #         'Is the object in the image similar to a ' + sampleResults["image_2_answer"] + '?',
    #         Image.open("Volcano.png")
    #     ]
    # )
    # questions.append(q.text)
    # sd.caption(q.text)

    sd.write("Question 3a Results:")
    q = questionDivider.send_message(
        message="Is this an accurate similarity for watches and rulers? " + sampleResults["similarity_qs"] + "."
    )
    questions.append(q.text)
    sd.caption(q.text)

    sd.write("Question 3b Results:")
    q = questionDivider.send_message(
        message="Is this a good response for the number of nickels in 60 cents:" + sampleResults["similarity_qs_2"] + "?"
    )
    questions.append(q.text)
    sd.caption(q.text)

    sd.write("Question 3c Results:")
    q = questionDivider.send_message(
        message="Is this the same as $6.55:" + sampleResults["similarity_qs_3"] + "?"
    )
    questions.append(q.text)
    sd.caption(q.text)

    sd.write("Question 4 Results:")
    #This might give an error
    q = questionDivider.send_message(
        message=sampleResults["animal_names"]
    )
    q = questionDivider.send_message(
        message="Given the list, how many are considered animals? How would you describe the other input? State this in a positive way"
    )
    questions.append(q.text)
    sd.caption(q.text)

    sd.write("Question 5 Results:")
    q = questionDivider.send_message(
        message="Given this correct answer key sequence of values" + str(sampleResults["sequence_answer"]) + ", are the user-made values in (" + str(sampleResults["sequence_qs_2"])+ ") similar to the correct answer?"
    )
    questions.append(q.text)
    sd.caption(q.text)

    sd.write("Question 6 Results:")
    q = questionDivider.send_message(
        message="Did the user write i am done: " + sampleResults["similarity_qs_3"] + "?"
    )
    questions.append(q.text)
    sd.caption(q.text)

    #Score
    sd.write("Final Score:")
    q = questionDivider.send_message(
        message = questions
    )
    q = questionDivider.send_message(
        message= "As a number value only, rate the user's performance on a scale of 0 to 30"
    )
    score = q.text
    sd.write(score)

    q = questionDivider.send_message(
        message= "Write out the score written as 1 number only"
    )
    score = q.text
    sd.subheader("Final score: " + score)

    q = questionDivider.send_message(
        message = "In two words, based on the score given, state whether the user is either Cognitively Impaired or Cognitively Sound"
    )
    mode = q.text
    sd.write(mode)

    if(mode == "Cognitively Impaired"):
        left, right = sd.columns(2)
        if left.button("Suggestions for Impaired Cognition", use_container_width=True, type="primary"):
            left.markdown("Opens intermediate page")
        if right.button("Other Suggestions", use_container_width=True, type="secondary"):
            right.markdown("Opens advanced page")

if st.button("Go to Game Hub for cognitively impaired"):
            st.markdown("""
                <meta http-equiv="refresh" content="2;url=/m_impaired" />
            """, unsafe_allow_html=True)

if st.button("Go to Game Hub for cognitively normal"):
            st.markdown("""
                <meta http-equiv="refresh" content="2;url=/m_normal" />
            """, unsafe_allow_html=True)




