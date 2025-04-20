import os
from urllib import response  
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=dotenv_path)


AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
REDIRECT_URI = os.getenv("REDIRECT_URI")

authorize_url = f"https://{AUTH0_DOMAIN}/authorize"
token_url = f"https://{AUTH0_DOMAIN}/oauth/token"
userinfo_url = f"https://{AUTH0_DOMAIN}/userinfo"

import streamlit as st
from authlib.integrations.requests_client import OAuth2Session
import json
from urllib.parse import urlencode, urlparse, parse_qs

from mongo import upsert_user

st.set_page_config(page_title="Auth0 Login")

if "auth_token" not in st.session_state:
    st.session_state["auth_token"] = None

if st.session_state["auth_token"] is None:
    params = {
        "client_id": AUTH0_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": "openid profile email",
    }

    login_url = f"{authorize_url}?{urlencode(params)}"

    signup_params = params.copy()
    signup_params["screen_hint"] = "signup"
    signup_params["prompt"] = "login" 
    signup_url = f"{authorize_url}?{urlencode(signup_params)}"

    logout_url = f"https://{AUTH0_DOMAIN}/v2/logout?client_id={AUTH0_CLIENT_ID}&returnTo={REDIRECT_URI}"

    st.title("Welcome Guest :)")
    st.markdown(f"[Login with Auth0]({login_url})")
    st.markdown(f"[Sign up with Auth0]({signup_url})")
    st.markdown(f"[Logout from Auth0 Session]({logout_url})")

    query_params = st.query_params
    if "code" in query_params:
        code = query_params.get("code")
        print("Auth code:", code)
        oauth = OAuth2Session(
            client_id=AUTH0_CLIENT_ID,
            client_secret=AUTH0_CLIENT_SECRET,
            redirect_uri=REDIRECT_URI,
            scope="openid profile email"
        )
        token = oauth.fetch_token(
            url=token_url,
            code=code,
            redirect_uri=REDIRECT_URI,
            auth=(AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET)
        )
        st.session_state["auth_token"] = token

        st.query_params.clear()
        st.rerun()

else:
    oauth = OAuth2Session(
            client_id=AUTH0_CLIENT_ID,
            client_secret=AUTH0_CLIENT_SECRET,
            redirect_uri=REDIRECT_URI,
            scope="openid profile email"
    )
    oauth.token = st.session_state["auth_token"]
    resp = oauth.get(userinfo_url)
    profile = resp.json() 

    upsert_user(profile) 

    st.title(f"Welcome {profile.get('name', 'User')} :)")
    st.json(profile)

    if st.button("Logout"):
        st.session_state["auth_token"] = None
        st.rerun()

def build_oauth_session():
    return OAuth2Session(
        client_id=AUTH0_CLIENT_ID,
        client_secret=AUTH0_CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope="openid profile email"
    )