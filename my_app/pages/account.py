import streamlit as st

import firebase_admin
from firebase_admin import credentials,firestore,auth
import time
import os

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

try:
    firebase_admin.get_app()
except ValueError:
    cred = credentials.Certificate("hackdemo-b2b14-a75cadbb8a8c.json")

    firebase_admin.initialize_app(cred)


def app():
    st.title('Welcome to Alzheimer Treatment Center')

    choice = st.selectbox('Login/Sign up,',['Login', 'Sign up'] )

    email = st.text_input('Email Address')
    password = st.text_input('Password', type = 'password')

    if choice == 'Login':
        if st.button('Login'):
            user = auth.get_user_by_email(email)
            st.session_state['user_id'] = user.uid
            st.success('Login successful! Redirecting...')

    if choice == 'Sign up':
        username = st.text_input("Choose a unique username")
        if st.button('Create my account'):
            try:
                user = auth.create_user(email=email, password=password)
                user_name = user.uid
                st.session_state["user_name"] = username
                st.success('Account created successfully!')
                st.markdown("Please log in using your email and password.")
                st.balloons()
                st.markdown("""
                    <meta http-equiv="refresh" content="2;url=/intake" />
                """, unsafe_allow_html=True)
            except:
                st.warning('Error creating account. Try a different email or username.')

    # After login
    if 'user_id' in st.session_state:
        st.info(f"You're logged in as `{st.session_state['user_id']}`")
        st.session_state.account_complete = True
        # You can replace this with navigation logic
        if st.button("Go to Intake Form"):
            st.markdown("""
                <meta http-equiv="refresh" content="2;url=/data_view" />
            """, unsafe_allow_html=True)
            
if __name__ == '__main__':
    app()