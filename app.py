
import streamlit as st
import json
import os
from frontend.landing_ui import render_landing
from frontend.chat_ui import render_chat
from frontend.sidebar import render_sidebar
from database import SessionLocal
from models import User
from streamlit_cookies_manager import EncryptedCookieManager
st.set_page_config(
    page_title="VizTalk",
    layout="wide",
    initial_sidebar_state="expanded"
)

cookies = EncryptedCookieManager(
    prefix="viztalk_",
    password="my_secret_password"
)

if not cookies.ready():
    st.stop()



# ── GLOBAL BASE STYLES ──
st.markdown("""
<style>
*, *::before, *::after { box-sizing: border-box; }

[data-testid="stAppViewContainer"] {
    background: #080C14 !important;
    font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
}
[data-testid="stAppViewBlockContainer"] {
    background: transparent !important;
    max-width: 1100px;
}
header[data-testid="stHeader"] { background: transparent !important; }

#MainMenu, footer { visibility: hidden; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #0D1117 !important;
    border-right: 1px solid rgba(255,255,255,0.05) !important;
}
section[data-testid="stSidebar"] * {
    color: #94A3B8 !important;
    font-family: 'DM Sans', sans-serif !important;
}


section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #E2E8F0 !important;
    font-family: 'Syne', sans-serif !important;
}

/* Sidebar expand arrow — bright and always visible */
[data-testid="stSidebarCollapsedControl"] {
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    width: 32px !important;
    background: #3B82F6 !important;
    border-radius: 0 8px 8px 0 !important;
    border: none !important;
    z-index: 9999 !important;
}
[data-testid="stSidebarCollapsedControl"] button {
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    pointer-events: all !important;
    cursor: pointer !important;
    width: 100% !important;
    height: 100% !important;
    background: transparent !important;
    border: none !important;
}
[data-testid="stSidebarCollapsedControl"] svg {
    fill: white !important;
    visibility: visible !important;
    width: 18px !important;
    height: 18px !important;
}
section[data-testid="stSidebar"] .stButton > button {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    color: #94A3B8 !important;
    border-radius: 8px !important;
    width: 100% !important;
    text-align: left !important;
    font-size: 13px !important;
    font-family: 'DM Sans', sans-serif !important;
    transition: all 0.2s !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(59,130,246,0.1) !important;
    border-color: rgba(59,130,246,0.3) !important;
    color: #93C5FD !important;
}

/* Global inputs */
[data-baseweb="input"] input {
    background: rgba(255,255,255,0.04) !important;
    color: #E2E8F0 !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
}
[data-baseweb="input"] input::placeholder { color: #64748B !important; }
[data-baseweb="input"] input:focus {
    border-color: rgba(59,130,246,0.5) !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,0.1) !important;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.02) !important;
    border: 1px dashed rgba(255,255,255,0.1) !important;
    border-radius: 12px !important;
}
[data-testid="stFileUploaderDropzone"] { background: transparent !important; }
[data-testid="stFileUploader"] * { color: #64748B !important; font-family: 'DM Sans', sans-serif !important; }

</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ──
if "page" not in st.session_state:
    st.session_state.page = "landing"

if "user" not in st.session_state:
    st.session_state.user = cookies.get("user")


# ════════════════════════════════
#  LANDING PAGE
# ════════════════════════════════
if st.session_state.page == "landing":
    render_landing()


# ════════════════════════════════
#  LOGIN PAGE
# ════════════════════════════════
elif st.session_state.page == "login":

    st.markdown("""
    <style>
    /* Blobs for login too */
    .login-blob-1 {
        position: fixed; width: 500px; height: 500px;
        background: rgba(59,130,246,0.12); border-radius: 50%;
        filter: blur(100px); top: -150px; left: -100px;
        pointer-events: none; z-index: 0;
    }
    .login-blob-2 {
        position: fixed; width: 400px; height: 400px;
        background: rgba(139,92,246,0.1); border-radius: 50%;
        filter: blur(100px); bottom: -100px; right: -100px;
        pointer-events: none; z-index: 0;
    }

    /* Login card */
    .login-card {
        background: rgba(255,255,255,0.02);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 20px;
        padding: 48px 44px;
        max-width: 420px;
        margin: 60px auto 0;
        position: relative;
        z-index: 5;
        backdrop-filter: blur(20px);
    }
    .login-logo {
        font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
        font-size: 26px;
        font-weight: 800;
        background: linear-gradient(135deg, #60A5FA, #A78BFA);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 6px;
    }
    .login-tagline {
        font-size: 14px;
        color: #94A3B8;
        text-align: center;
        margin-bottom: 36px;
        font-weight: 400;
    }
    .login-section-title {
        font-size: 15px;
        font-weight: 600;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        color: #3B82F6 !important;
        margin-bottom: 16px !important;
    }

    /* Input labels */
    label {
        color: #CBD5E1 !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        font-family: 'DM Sans', sans-serif !important;
    }

    /* Divider */
    .login-divider {
        border: none;
        height: 1px;
        background: rgba(255,255,255,0.06);
        margin: 28px 0;
    }

    /* Login / Register buttons */
    .stButton > button {
        background: linear-gradient(135deg, #3B82F6, #8B5CF6) !important;
        color: white !important;
        border: none !important;
        padding: 6px 14px !important;
        border-radius: 8px !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 12px !important;
        font-weight: 600 !important;
        width: auto !important;
        white-space: nowrap !important;
        letter-spacing: 0.3px !important;
        box-shadow: 0 0 24px rgba(59,130,246,0.2) !important;
        transition: all 0.25s ease !important;
    }
    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 0 40px rgba(59,130,246,0.38) !important;
    }

    /* Alert */
    [data-testid="stAlert"] {
        border-radius: 10px !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 13px !important;
    }

    /* Back link button */
    .back-btn {
        display: flex;
        align-items: center;
        gap: 6px;
        color: #475569 !important;
        font-size: 13px;
        cursor: pointer;
        margin-bottom: 32px;
        width: fit-content;
        font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
        background: none;
        border: none;
        padding: 0;
    }
    </style>

    <div class="login-blob-1"></div>
    <div class="login-blob-2"></div>
    """, unsafe_allow_html=True)

    if st.session_state.get("login_alert"):
        st.warning("⚠️ Please log in to continue.")
        st.session_state.login_alert = False

    # Back button
    if st.button("Back to Home"):
        st.session_state.page = "landing"
        st.rerun()

    # Centered login card wrapper
    _, center, _ = st.columns([1, 2, 1])

    with center:
        st.markdown("""
        <div class="login-card">
            <div class="login-logo">Login/SignUP</div>
            <div class="login-tagline">Sign in to explore your data</div>
        </div>
        """, unsafe_allow_html=True)

        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")

        st.markdown('<hr class="login-divider">', unsafe_allow_html=True)

        # LOGIN
        login_label, login_btn = st.columns([1.2, 1])
        with login_label:
            st.markdown('<div class="login-section-title" style="padding-top:10px;">Existing Account?</div>', unsafe_allow_html=True)
        with login_btn:
            if st.button("Sign In", key="signin_btn"):
                db = SessionLocal()

                user = db.query(User).filter(
                    User.username == username,
                    User.password == password
                ).first()

                if user:
                    st.session_state.user = username
                    cookies["user"] = username
                    cookies.save()
                    st.session_state.page = "chat"
                    st.success("✓ Signed in successfully")
                    st.rerun()
                else:
                    st.error("Invalid username or password.")

        st.markdown('<hr class="login-divider">', unsafe_allow_html=True)

        # REGISTER
        reg_label, reg_btn = st.columns([1.2, 1])
        with reg_label:
            st.markdown('<div class="login-section-title" style="padding-top:10px;">New Here?</div>', unsafe_allow_html=True)
        with reg_btn:
            if st.button("Register", key="register_btn"):
                # users = load_users()
                # if not username:
                #     st.warning("Please enter a username.")
                # elif username in users:
                #     st.warning("Username already exists. Try signing in.")
                # else:
                #     users[username] = password
                #     save_users(users)
                db = SessionLocal()

                if not username:
                    st.warning("Please enter a username.")

                else:
                    existing_user = db.query(User).filter(
                        User.username == username
                    ).first()

                    if existing_user:
                        st.warning("Username already exists. Try signing in.")

                    else:
                        new_user = User(username=username, password=password)

                        db.add(new_user)
                        db.commit()

                        st.success("✓ Account created! You can now sign in.")
                    st.success("✓ Account created! You can now sign in.")


# ════════════════════════════════
#  CHAT PAGE
# ════════════════════════════════
elif st.session_state.page == "chat":

    if not st.session_state.user:
        st.session_state.login_alert = True
        st.session_state.page = "login"
        st.rerun()

    render_sidebar()
    render_chat()