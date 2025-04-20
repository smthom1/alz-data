import streamlit as st
import pandas as pd
import pymongo
import certifi
from datetime import datetime
import os
import google.generativeai as genai
from urllib.parse import unquote

## TODO: identify and pull respective user information to get data

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

genai.configure(api_key=os.getenv("API_KEY"))
models = genai.list_models()

query_params = st.query_params
if "q" in query_params:
    user_question = unquote(query_params["q"][0])
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(user_question)
        st.markdown(response.text)
    except Exception as e:
        st.error(f"Error fetching AI response: {e}")
    st.stop()  # Stop here so rest of the app doesn't load on fetch

st.title("Data Viewer")

# MongoDB connection string
uri = os.getenv("MONGO_URI")

# Create MongoClient with the certifi certificates
client = pymongo.MongoClient(uri, tlsCAFile=certifi.where())

# Access the database and collection
db = client["store"]
collection = db["products"]

# Fetch all records for the given auth_user
auth_user_id = "38373892374"  # Replace with actual user ID
data = list(collection.find({"user_auth": auth_user_id}))
print(data)

# Convert JSON data to DataFrame
df = pd.DataFrame(data)

# Ensure submission_time is converted properly
if "submission_time" in df.columns:
    df["submission_time"] = df["submission_time"].apply(lambda x: x.get("$date") if isinstance(x, dict) else x)
    df["submission_time"] = pd.to_datetime(df["submission_time"])

# Streamlit App
st.title("User Progress Over Time")

# Select metrics to visualize
metrics = ["memory_problems", "balance_problems", "depression", "stroke_history.yes"]

# Create time-based charts
for metric in metrics:
    if metric in df.columns:
        st.subheader(f"Trend of {metric} Over Time")
        st.line_chart(df[["submission_time", metric]].set_index("submission_time"))

# Display raw data
st.subheader("Raw Data")
st.dataframe(df)

if st.button("Go back to input form"):
    os.system("streamlit run mongo.py")

# --- Popup AI Assistant in Streamlit (no JS fetch needed) ---

# Initialize chat state
if "show_chat" not in st.session_state:
    st.session_state.show_chat = False
if "ai_response" not in st.session_state:
    st.session_state.ai_response = ""

# Floating button to toggle popup
with st.container():
    st.markdown("""
    <style>
    .floating-ai-btn {
        position: fixed;
        bottom: 20px;
        right: 20px;
        background-color: #FF69B4;
        color: white;
        padding: 12px 18px;
        border-radius: 30px;
        cursor: pointer;
        font-size: 16px;
        font-weight: bold;
        text-align: center;
        z-index: 1000;
        box-shadow: 2px 4px 6px rgba(0,0,0,0.2);
    }
    </style>
    """, unsafe_allow_html=True)

    if st.button("AI Assistant", key="ai_btn", help="Toggle AI Assistant"):
        st.session_state.show_chat = not st.session_state.show_chat

# AI popup window
if st.session_state.show_chat:
    with st.container():
        user_input = st.text_area("Ask the AI", key="chat_input", label_visibility="collapsed", height=70)
        if st.button("Send", key="chat_send"):
            if user_input.strip():
                try:
                    model = genai.GenerativeModel("gemini-2.0-flash")
                    response = model.generate_content(user_input)
                    st.session_state.ai_response = response.text
                except Exception as e:
                    st.session_state.ai_response = f"Error: {e}"

        if st.session_state.ai_response:
            st.markdown("---")
            st.markdown(f"**Response:** {st.session_state.ai_response}")

        st.markdown("</div>", unsafe_allow_html=True)

