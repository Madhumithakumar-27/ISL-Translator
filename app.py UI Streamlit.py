Python 3.8.10 (tags/v3.8.10:3d8993a, May  3 2021, 11:48:03) [MSC v.1928 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
>>> import streamlit as st

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Sign Language App", layout="wide")

# ---------- UI DESIGN (CSS) ----------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #d1fae5, #a7f3d0, #fca5a5);
}
h1 {
    text-align: center;
}
.custom-card {
    padding: 30px;
    border-radius: 20px;
}
.stButton>button {
    width: 100%;
    height: 70px;
}
</style>
""", unsafe_allow_html=True)

# ---------- HOME PAGE UI ----------
def home():
    st.title("🤟 Sign Language Recognition System")
    st.caption("AI-powered real-time communication platform")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🚀 Features")
        st.markdown("- Real-time detection\n- Two-hand recognition")

    with col2:
        st.image("avatar.png")

    if st.button("User Login"):
        st.session_state.page = "user_login"

# ---------- LOGIN UI ----------
def user_login():
    st.title("User Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        st.success("Login clicked")

# ---------- REGISTER UI ----------
def register():
    st.title("Register")

    name = st.text_input("Name")
    email = st.text_input("Email")

    if st.button("Register"):
        st.success("Registered")

# ---------- DASHBOARD UI ----------
def dashboard():
    st.title("Dashboard")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Sign to Voice"):
            st.write("Open feature")

    with col2:
        if st.button("Voice to Sign"):
            st.write("Open feature")
