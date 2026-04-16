import streamlit as st
from db import get_connection
import cv2
import mediapipe as mp
import numpy as np
import pickle
import pandas as pd
import os

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Sign Language App", layout="wide")

st.markdown("""
<style>

/* ---------- MAIN BACKGROUND ---------- */
.stApp {
    background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 30%, #fca5a5 100%);
    font-family: 'Segoe UI', sans-serif;
}

/* ---------- HEADER ---------- */
h1 {
    color: #064e3b;
    font-size: 44px !important;
    font-weight: 800;
    text-align: center;
    letter-spacing: 1px;
}

/* ---------- SUBTEXT ---------- */
h3, h4 {
    color: #065f46;
}

/* ---------- CARD ---------- */
.custom-card {
    background: linear-gradient(135deg, rgba(255,255,255,0.9), rgba(255,255,255,0.6));
    padding: 30px;
    border-radius: 20px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    border-left: 6px solid #22c55e;
}

/* ---------- FEATURE LIST ---------- */
.custom-card ul {
    line-height: 2;
    font-size: 17px;
}

/* ---------- BUTTONS ---------- */
.stButton>button {
    width: 100%;
    height: 70px;
    font-size: 20px;
    font-weight: bold;
    border-radius: 18px;
    border: none;
    color: white;
    background: linear-gradient(135deg, #22c55e, #16a34a);
    box-shadow: 0 8px 20px rgba(34,197,94,0.5);
    transition: 0.3s ease;
}

/* Hover */
.stButton>button:hover {
    transform: scale(1.07);
    background: linear-gradient(135deg, #16a34a, #15803d);
}

/* ---------- INPUTS ---------- */
.stTextInput>div>div>input,
.stSelectbox>div>div {
    background-color: #ffffff;
    border-radius: 12px;
    border: 1px solid #cbd5e1;
}

/* ---------- TEXT ---------- */
p, li, label {
    color: #1f2937 !important;
}

/* ---------- DIVIDER ---------- */
.hr-line {
    border: none;
    height: 2px;
    background: linear-gradient(to right, #22c55e, #ef4444);
    margin: 25px 0;
}

/* ---------- IMAGE STYLE ---------- */
.hero-img {
    display: block;
    margin: auto;
    width: 250px;
    border-radius: 20px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.2);
}
/* Make layout spacing better */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Improve columns spacing */
.css-1kyxreq {
    gap: 30px;
}
/* Login form spacing */
input {
    height: 45px !important;
    font-size: 16px !important;
}

/* Improve card spacing */
.custom-card h3 {
    margin-bottom: 15px;
}
/* Bigger login container */
.custom-card {
    padding: 40px !important;
}

/* Center inputs spacing */
.stTextInput {
    margin-bottom: 15px;
}
/* SIDEBAR FULL DESIGN */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #064e3b, #022c22);
    padding: 20px;
}

/* Sidebar title */
section[data-testid="stSidebar"] h2 {
    color: white;
    font-size: 22px;
    margin-bottom: 20px;
}

/* Sidebar buttons */
.sidebar-btn {
    display: block;
    padding: 12px 15px;
    margin-bottom: 10px;
    border-radius: 12px;
    color: white;
    text-decoration: none;
    background: transparent;
    transition: 0.3s;
}

/* Active / hover */
.sidebar-btn:hover {
    background: linear-gradient(135deg, #22c55e, #16a34a);
}

/* Active selected */
.active-link {
    background: linear-gradient(135deg, #22c55e, #16a34a);
}

/* Card hover effect */
.custom-card {
    transition: 0.3s;
    cursor: pointer;
}

.custom-card:hover {
    transform: translateY(-5px) scale(1.02);
    box-shadow: 0 15px 35px rgba(0,0,0,0.25);
}

/* Dashboard spacing */
h1 {
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------- SESSION ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.username = None

# ---------- HOME PAGE ----------
def home():
    st.title("🤟 Sign Language Recognition System")
    st.caption("AI-powered real-time communication platform 🚀")

    st.markdown("<hr class='hr-line'>", unsafe_allow_html=True)

    # ---------- SIDE BY SIDE LAYOUT ----------
    col1, col2 = st.columns([1.2, 1])

    # LEFT SIDE → FEATURES
    with col1:
        st.markdown("""
        <div class='custom-card'>
        <h3>🚀 Project Features</h3>
        <ul>
            <li>⚡ Real-time Sign Detection using AI</li>
            <li>🤲 Two-Hand Gesture Recognition</li>
            <li>🔐 Secure Login System</li>
            <li>📊 Admin Dashboard with Data Insights</li>
            <li>🧠 Train Custom AI Model</li>
            <li>🔊 Auto Voice Output (Multi-language)</li>
            <li>🎭 Sign Avatar Generation</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    # RIGHT SIDE → IMAGE
    import base64

    def get_base64_image(image_path):
        with open(image_path, "rb") as img:
            return base64.b64encode(img.read()).decode()

    img_base64 = get_base64_image("avatar.png")

    with col2:
        st.markdown(f"""
            <img src="data:image/png;base64,{img_base64}"
            style="
                width: 100%;
                max-width: 630px;
                display: block;
                margin: auto;
                border-radius: 20px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            ">
        """, unsafe_allow_html=True)

    st.markdown("<hr class='hr-line'>", unsafe_allow_html=True)

    # ---------- BIG BUTTONS ----------
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("👤 User Login", use_container_width=True):
            st.session_state.page = "user_login"

    with col2:
        if st.button("📝 Register", use_container_width=True):
            st.session_state.page = "register"

    with col3:
        if st.button("🔑 Admin Login", use_container_width=True):
            st.session_state.page = "admin_login"

# ---------- ADMIN LOGIN ----------
def admin_login():
    st.title("🔐 Admin Panel")
    st.caption("Secure access to system control")

    st.markdown("<hr class='hr-line'>", unsafe_allow_html=True)

    # ---------- SIDE BY SIDE ----------
    col1, col2 = st.columns([1.2, 1])

    # ---------- LEFT → BIG PARAGRAPH ----------
    with col1:
        st.markdown("""
        <div class='custom-card' style='padding:50px;'>
            <h2 style='font-size:30px; line-height:1.6; text-align:left;'>
            ⚡ Manage your entire system with powerful admin controls, monitor user activity,
            train intelligent AI models, and handle sign language avatars seamlessly in one place.
            </h2>
        </div>
        """, unsafe_allow_html=True)

    # ---------- RIGHT → BIG LOGIN ----------
    with col2:
        st.markdown("""
        <div class='custom-card' style='padding:50px; text-align:center;'>
            <h2>🔑 Admin Login</h2>
        </div>
        """, unsafe_allow_html=True)

        username = st.text_input("👤 Username")
        password = st.text_input("🔒 Password", type="password")

        if st.button("🚀 Login to Dashboard", use_container_width=True):
            if username == "admin" and password == "admin":
                st.session_state.logged_in = True
                st.session_state.role = "admin"
                st.session_state.page = "admin_dashboard"
            else:
                st.error("❌ Invalid credentials")

    st.markdown("<hr class='hr-line'>", unsafe_allow_html=True)

    # ---------- BACK BUTTON CENTER ----------
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("⬅ Back to Home", use_container_width=True):
            st.session_state.page = "home"

# ---------- ADMIN DASHBOARD ----------
def admin_dashboard():

    st.markdown("<h1>📊 Admin Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<hr class='hr-line'>", unsafe_allow_html=True)

    # ---------- NAVIGATION CARDS ----------
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class='custom-card'>
            <h3>🎯 Train Model</h3>
            <p>Capture gesture data and train your AI model for sign recognition.</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Go to Training", use_container_width=True):
            st.session_state.page = "train_model"

    with col2:
        st.markdown("""
        <div class='custom-card'>
            <h3>🎭 Add Avatar</h3>
            <p>Upload and manage sign avatars for visual communication.</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Manage Avatars", use_container_width=True):
            st.session_state.page = "add_avatar"

    with col3:
        st.markdown("""
        <div class='custom-card'>
            <h3>🚪 Logout</h3>
            <p>Securely logout from admin panel and return to home page.</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.page = "home"

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------- USER TABLE ----------
    st.markdown("<h3>👥 Registered Users</h3>", unsafe_allow_html=True)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, email, mobile, age, gender, dob, location, username 
        FROM users
    """)

    users = cursor.fetchall()

    import pandas as pd
    columns = ["ID", "Name", "Email", "Mobile", "Age", "Gender", "DOB", "Location", "Username"]
    df = pd.DataFrame(users, columns=columns)

    st.dataframe(df, use_container_width=True)

def add_avatar_page():

    # ---------- BACK BUTTON ----------
    col1, col2 = st.columns([1,5])
    with col1:
        if st.button("⬅ Dashboard"):
            st.session_state.page = "admin_dashboard"

    # ---------- HEADER ----------
    st.markdown("<h1>🎭 Avatar Management</h1>", unsafe_allow_html=True)
    st.markdown("<hr class='hr-line'>", unsafe_allow_html=True)

    # ---------- INPUT SECTION (CLEAN - NO EXTRA BOX) ----------
    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        sign_name = st.text_input("✍ Enter Sign Name")

        uploaded_file = st.file_uploader(
            "📁 Upload GIF/Image", type=["gif", "png", "jpg"]
        )

        # ---------- PREVIEW ----------
        if uploaded_file is not None:
            st.image(uploaded_file, caption="Preview", width=250)

        # ---------- SAVE ----------
        if st.button("🚀 Save Avatar", use_container_width=True):

            if sign_name.strip() == "" or uploaded_file is None:
                st.error("❌ Provide both sign name and file")
                return

            if not os.path.exists("avatars"):
                os.makedirs("avatars")

            clean_name = sign_name.lower().strip().replace(" ", "_")
            file_path = f"avatars/{clean_name}.gif"

            with open(file_path, "wb") as f:
                f.write(uploaded_file.read())

            st.success(f"✅ Avatar saved for '{sign_name}'")

    # ---------- AVATAR DISPLAY ----------
    st.markdown("<hr class='hr-line'>", unsafe_allow_html=True)
    st.markdown("<h3>🖐 Available Avatars</h3>", unsafe_allow_html=True)

    if os.path.exists("avatars"):
        avatar_files = os.listdir("avatars")

        if len(avatar_files) == 0:
            st.info("No avatars added yet.")
        else:
            cols = st.columns(4)

            for i, file in enumerate(avatar_files):
                path = f"avatars/{file}"
                name = file.replace(".gif", "")

                with cols[i % 4]:
                    # ---------- FIXED INDENT ----------
                    if os.path.exists(path):
                        st.image(path, width=150)

                    st.caption(name)

    else:
        st.info("No avatars folder found.")

    # ---------- BOTTOM ACTIONS ----------
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🎯 Go to Training", use_container_width=True):
            st.session_state.page = "train_model"

    with col2:
        if st.button("📊 Back to Dashboard", use_container_width=True):
            st.session_state.page = "admin_dashboard"
        
def train_model_page():

    # ---------- BACK BUTTON ----------
    colA, colB = st.columns([1,5])
    with colA:
        if st.button("⬅ Dashboard"):
            st.session_state.page = "admin_dashboard"

    # ---------- HEADER ----------
    st.markdown("<h1>🎯 Train AI Model</h1>", unsafe_allow_html=True)
    st.markdown("<hr class='hr-line'>", unsafe_allow_html=True)

    # ---------- INFO CARDS ----------
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class='custom-card'>
            <h3>📸 Capture</h3>
            <p>Capture real-time gesture data using webcam.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='custom-card'>
            <h3>🧠 Train</h3>
            <p>Train AI model with collected gesture dataset.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------- MAIN TRAIN CARD ----------
    st.markdown("""
    <div class='custom-card' style='padding:30px; text-align:center;'>
        <h2>🎥 Live Training System</h2>
    </div>
    """, unsafe_allow_html=True)

    # ---------- INPUT ----------
    sign_name = st.text_input("✍ Enter Sign Name")

    # ---------- BUTTONS ----------
    col1, col2, col3 = st.columns(3)

    start = col1.button("▶ Start Camera", use_container_width=True)
    stop = col2.button("⏹ Stop Camera", use_container_width=True)
    train_btn = col3.button("🚀 Train Model", use_container_width=True)

    frame_window = st.empty()

    # ---------- SESSION ----------
    if "run_cam" not in st.session_state:
        st.session_state.run_cam = False

    if "data" not in st.session_state:
        st.session_state.data = []
        st.session_state.labels = []
        st.session_state.sample_count = 0

    if start:
        st.session_state.run_cam = True

    if stop:
        st.session_state.run_cam = False

    # ---------- CAMERA ----------
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(max_num_hands=2)
    mp_draw = mp.solutions.drawing_utils

    def normalize(landmarks):
        arr = np.array(landmarks).reshape(-1, 3)
        base = arr[0]
        arr = arr - base
        norm = np.linalg.norm(arr)
        if norm != 0:
            arr = arr / norm
        return arr.flatten()

    if st.session_state.run_cam:
        cap = cv2.VideoCapture(0)
        import time
        start_time = time.time()

        while st.session_state.run_cam:
            ret, frame = cap.read()
            frame = cv2.flip(frame, 1)

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = hands.process(image)

            landmarks = []

            if result.multi_hand_landmarks:
                for hand_landmarks in result.multi_hand_landmarks:
                    mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                    for lm in hand_landmarks.landmark:
                        landmarks.extend([lm.x, lm.y, lm.z])

            while len(landmarks) < 126:
                landmarks.append(0)

            frame_window.image(frame, channels="BGR")

            if sign_name and len(landmarks) == 126:
                norm = normalize(landmarks)
                st.session_state.data.append(norm)
                st.session_state.labels.append(sign_name)
                st.session_state.sample_count += 1

            if time.time() - start_time > 20:
                st.session_state.run_cam = False
                break

        cap.release()
        st.success(f"✅ Captured {st.session_state.sample_count} samples!")

    # ---------- TRAIN ----------
    if train_btn:
        if len(st.session_state.data) == 0:
            st.error("❌ No data captured!")
            return

        df = pd.DataFrame(st.session_state.data)
        df["label"] = st.session_state.labels

        df.to_csv("dataset.csv", mode="a", header=not os.path.exists("dataset.csv"), index=False)

        from sklearn.ensemble import RandomForestClassifier

        data = pd.read_csv("dataset.csv")
        X = data.iloc[:, :-1]
        y = data.iloc[:, -1]

        model = RandomForestClassifier(n_estimators=300, max_depth=20)
        model.fit(X, y)

        pickle.dump(model, open("model.pkl", "wb"))

        st.success("🎉 Model trained successfully!")

        st.session_state.data = []
        st.session_state.labels = []
        st.session_state.sample_count = 0

    # ---------- TRAINED SIGNS TABLE ----------
    st.markdown("<hr class='hr-line'>", unsafe_allow_html=True)
    st.markdown("<h3>📊 Trained Signs</h3>", unsafe_allow_html=True)

    if os.path.exists("dataset.csv"):
        data = pd.read_csv("dataset.csv")

        if "label" in data.columns:
            unique_signs = data["label"].value_counts().reset_index()
            unique_signs.columns = ["Sign Name", "Samples"]

            st.dataframe(unique_signs, use_container_width=True)
        else:
            st.info("No trained signs available yet.")
    else:
        st.info("No dataset found. Train model first.")
# ---------- USER REGISTER ----------
def register():
    st.markdown("<h1 style='text-align:center;'>📝 Create Account</h1>", unsafe_allow_html=True)

    st.markdown("<hr class='hr-line'>", unsafe_allow_html=True)

    # ---------- CENTER CONTAINER ----------
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        # ---------- REGISTER CARD ----------
        st.markdown("""
        <div class='custom-card' style='padding:50px;'>
        """, unsafe_allow_html=True)

        # ---------- TWO COLUMN FORM ----------
        c1, c2 = st.columns(2)

        with c1:
            name = st.text_input("👤 Name")
            email = st.text_input("📧 Email")
            mobile = st.text_input("📱 Mobile")
            age = st.number_input("🎂 Age", min_value=1)

        with c2:
            gender = st.selectbox("⚧ Gender", ["Male", "Female", "Other"])
            dob = st.date_input("📅 Date of Birth")
            location = st.text_input("📍 Location")
            username = st.text_input("🆔 Username")

        password = st.text_input("🔒 Password", type="password")

        # ---------- REGISTER BUTTON ----------
        if st.button("🚀 Register", use_container_width=True):
            conn = get_connection()
            cursor = conn.cursor()

            query = """
            INSERT INTO users 
            (name, email, mobile, age, gender, dob, location, username, password)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """

            values = (name, email, mobile, age, gender, dob, location, username, password)

            try:
                cursor.execute(query, values)
                conn.commit()
                st.success("✅ Registered Successfully")
            except:
                st.error("❌ Username already exists")

        st.markdown("</div>", unsafe_allow_html=True)

        # ---------- BOTTOM LINKS ----------
        colA, colB = st.columns(2)

        with colA:
            if st.button("🔐 Login", use_container_width=True):
                st.session_state.page = "user_login"

        with colB:
            if st.button("⬅ Home", use_container_width=True):
                st.session_state.page = "home"

# ---------- USER LOGIN ----------
def user_login():
    st.title("👤 User Access")
    st.caption("Login or create your account to continue 🚀")

    st.markdown("<hr class='hr-line'>", unsafe_allow_html=True)

    # ---------- SIDE BY SIDE ----------
    col1, col2 = st.columns([1.2, 1])

    # ---------- LEFT → BIG MINIMAL TEXT ----------
    with col1:
        st.markdown("""
        <div class='custom-card' style='padding:50px;'>
            <h2 style='font-size:30px; line-height:1.7;'>
            ✋ Experience real-time sign language recognition, convert gestures into voice instantly,
            and communicate seamlessly using AI-powered tools designed for speed, accuracy, and accessibility.
            </h2>

        </div>
        """, unsafe_allow_html=True)

    # ---------- RIGHT → BIG LOGIN BOX ----------
    with col2:
        st.markdown("""
        <div class='custom-card' style='padding:50px; text-align:center;'>
            <h2>🔐 User Login</h2>
        </div>
        """, unsafe_allow_html=True)

        username = st.text_input("👤 Username")
        password = st.text_input("🔒 Password", type="password")

        if st.button("🚀 Login", use_container_width=True):
            conn = get_connection()
            cursor = conn.cursor()

            query = "SELECT * FROM users WHERE username=%s AND password=%s"
            cursor.execute(query, (username, password))
            user = cursor.fetchone()

            if user:
                st.session_state.logged_in = True
                st.session_state.role = "user"
                st.session_state.username = username
                st.session_state.page = "user_dashboard"
            else:
                st.error("❌ Invalid credentials")

        # ---------- REGISTER BUTTON ----------
        if st.button("📝 Create New Account", use_container_width=True):
            st.session_state.page = "register"

    st.markdown("<hr class='hr-line'>", unsafe_allow_html=True)

    # ---------- BACK BUTTON ----------
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("⬅ Back to Home", use_container_width=True):
            st.session_state.page = "home"
# ---------- USER DASHBOARD ----------
def user_dashboard():

    # ---------- HEADER ----------
    st.markdown(f"<h1>👋 Welcome, {st.session_state.username}</h1>", unsafe_allow_html=True)
    st.markdown("<hr class='hr-line'>", unsafe_allow_html=True)

    # ---------- FEATURE CARDS ----------
    col1, col2, col3 = st.columns(3)

    # ---------- SIGN TO VOICE ----------
    with col1:
        st.markdown("""
        <div class='custom-card'>
            <h3>✋ Sign to Voice</h3>
            <p>Convert hand gestures into speech instantly using AI recognition.</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Start Sign Detection", use_container_width=True):
            st.session_state.page = "sign_to_voice"

    # ---------- VOICE TO SIGN ----------
    with col2:
        st.markdown("""
        <div class='custom-card'>
            <h3>🗣 Voice to Sign</h3>
            <p>Convert voice or text into animated sign avatars for communication.</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Start Voice Conversion", use_container_width=True):
            st.session_state.page = "voice_to_sign"

    # ---------- LOGOUT ----------
    with col3:
        st.markdown("""
        <div class='custom-card'>
            <h3>🚪 Logout</h3>
            <p>Securely logout from your account and return to home page.</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.page = "home"

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------- OPTIONAL INFO SECTION ----------
    st.markdown("<h3>📊 Your Features</h3>", unsafe_allow_html=True)

    st.markdown("""
    <div class='custom-card'>
        <p>
        Use AI-powered tools to convert sign language into speech and translate voice into sign avatars.
        This system enables seamless communication and accessibility for everyone.
        </p>
    </div>
    """, unsafe_allow_html=True)

from googletrans import Translator
from gtts import gTTS
import base64
import io
import time

# ---------- AUTO PLAY AUDIO (NO UI PLAYER) ----------
def autoplay_audio(text, lang_code):
    tts = gTTS(text=text, lang=lang_code)

    mp3_fp = io.BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)

    audio_bytes = mp3_fp.read()
    b64 = base64.b64encode(audio_bytes).decode()

    audio_html = f"""
        <audio autoplay>
        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
    """

    st.markdown(audio_html, unsafe_allow_html=True)

def sign_to_voice_page():

    # ---------- BACK BUTTON ----------
    colA, colB = st.columns([1,5])
    with colA:
        if st.button("⬅ Dashboard"):
            st.session_state.page = "user_dashboard"

    # ---------- HEADER ----------
    st.markdown("<h1>✋ Sign to Voice</h1>", unsafe_allow_html=True)
    st.markdown("<hr class='hr-line'>", unsafe_allow_html=True)

    # ---------- INFO CARDS ----------
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class='custom-card'>
            <h3>📸 Live Detection</h3>
            <p>Capture hand gestures in real-time using webcam.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='custom-card'>
            <h3>🔊 Voice Output</h3>
            <p>Automatically converts detected signs into speech instantly.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------- MAIN CONTROL PANEL ----------
    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        st.markdown("""
        <div class='custom-card' style='padding:30px; text-align:center;'>
            <h2>🎥 Live Sign Recognition</h2>
        </div>
        """, unsafe_allow_html=True)

        languages = {
            "English": "en",
            "Tamil": "ta",
            "Hindi": "hi",
            "Malayalam": "ml",
            "Telugu": "te",
            "Kannada": "kn",
            "French": "fr",
            "German": "de",
            "Spanish": "es",
            "Chinese": "zh-cn"
        }

        lang = st.selectbox("🌍 Language", list(languages.keys()))

        colA, colB = st.columns(2)
        with colA:
            start = st.button("▶ Start Camera", use_container_width=True)
        with colB:
            stop = st.button("⏹ Stop Camera", use_container_width=True)

        frame_placeholder = st.empty()
        result_box = st.empty()

    # -------- SESSION --------
    if "run_cam" not in st.session_state:
        st.session_state.run_cam = False

    if start:
        st.session_state.run_cam = True

    if stop:
        st.session_state.run_cam = False

    # Prevent repeating same word continuously (optional but recommended)
    if "last_spoken" not in st.session_state:
        st.session_state.last_spoken = ""

    # -------- LOAD MODEL --------
    if not os.path.exists("model.pkl"):
        st.error("Train model first!")
        return

    model = pickle.load(open("model.pkl", "rb"))

    mp_hands = mp.solutions.hands
    mp_draw = mp.solutions.drawing_utils
    hands = mp_hands.Hands(max_num_hands=2)

    translator = Translator()

    def normalize(landmarks):
        arr = np.array(landmarks).reshape(-1, 3)
        base = arr[0]
        arr = arr - base
        norm = np.linalg.norm(arr)
        if norm != 0:
            arr = arr / norm
        return arr.flatten()

    # -------- CAMERA --------
    if st.session_state.run_cam:
        cap = cv2.VideoCapture(0)

        for _ in range(500):
            if not st.session_state.run_cam:
                break

            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            frame = cv2.resize(frame, (640, 480))

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = hands.process(image)

            landmarks = []
            hand_detected = False

            if result.multi_hand_landmarks:
                hand_detected = True

                for hand_landmarks in result.multi_hand_landmarks:
                    mp_draw.draw_landmarks(
                        frame,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS
                    )

                    for lm in hand_landmarks.landmark:
                        landmarks.extend([lm.x, lm.y, lm.z])

            while len(landmarks) < 126:
                landmarks.append(0)

            frame_placeholder.image(frame, channels="BGR")

            # -------- DETECTION --------
            if hand_detected and len(landmarks) == 126:

                norm = normalize(landmarks)

                pred = model.predict(pd.DataFrame([norm]))[0]

                translated = translator.translate(
                    pred, dest=languages[lang]
                ).text

                result_box.markdown(f"""
                <div style="
                    text-align: center;
                    margin-top: 20px;
                ">
                    <h1 style="
                        font-size: 60px;
                        font-weight: 800;
                        color: #ef4444;
                        letter-spacing: 2px;
                        text-shadow: 2px 2px 10px rgba(0,0,0,0.3);
                    ">
                        {translated}
                    </h1>
                </div>
                """, unsafe_allow_html=True)

                # 🔥 TRUE AUTOPLAY VOICE (NO BUTTON, NO PLAYER)
                if translated != st.session_state.last_spoken:
                    autoplay_audio(translated, languages[lang])
                    st.session_state.last_spoken = translated

            time.sleep(0.03)

        cap.release()

    # ---------- BOTTOM ACTION ----------
    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("⬅ Back to Dashboard", use_container_width=True):
        st.session_state.page = "user_dashboard"

import speech_recognition as sr


def play_gif(file_path, width=350):
    import base64

    with open(file_path, "rb") as f:
        data = f.read()

    b64 = base64.b64encode(data).decode()

    gif_html = f"""
    <div style="
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        margin-bottom: 10px;
    ">
        <img 
            src="data:image/gif;base64,{b64}" 
            style="
                width: {width}px;
                max-width: 100%;
                height: auto;
                border-radius: 15px;
                box-shadow: 0px 8px 20px rgba(0,0,0,0.3);
                transition: 0.3s;
            "
        />
    </div>
    """

    st.markdown(gif_html, unsafe_allow_html=True)


def speech_to_text_js():
    st.components.v1.html("""
    <script>
    const recognition = new webkitSpeechRecognition();
    recognition.lang = "en-US";
    recognition.start();

    recognition.onresult = function(event) {
        const text = event.results[0][0].transcript;
        window.parent.postMessage({type: "speech", text: text}, "*");
    };
    </script>
    """, height=0)



def voice_to_sign_page():

    import os
    import tempfile
    import speech_recognition as sr
    from pydub import AudioSegment
    from streamlit_mic_recorder import mic_recorder

    # ---------- BACK BUTTON ----------
    colA, colB = st.columns([1,5])
    with colA:
        if st.button("⬅ Dashboard"):
            st.session_state.page = "user_dashboard"

    # ---------- HEADER ----------
    st.markdown("<h1>🗣 Voice to Sign Avatar</h1>", unsafe_allow_html=True)
    st.markdown("<hr class='hr-line'>", unsafe_allow_html=True)

    # ---------- INFO CARDS ----------
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class='custom-card'>
            <h3>📝 Text Input</h3>
            <p>Enter text and convert it into sign language avatars.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='custom-card'>
            <h3>🎤 Live Microphone</h3>
            <p>Speak directly using browser mic (fully working).</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------- INPUT SECTION ----------
    col1, col2, col3 = st.columns([1,2,1])

    with col2:

        # ---------- TEXT INPUT ----------
        text_input = st.text_input("✍ Type or Speak")

        # ---------- MIC RECORDER ----------
        audio = mic_recorder(
            start_prompt="🎤 Start Recording",
            stop_prompt="⏹ Stop Recording",
            just_once=True,
            use_container_width=True
        )

        voice_text = ""

        # ---------- PROCESS AUDIO (FINAL FIX) ----------
        if audio and "bytes" in audio:

            recognizer = sr.Recognizer()

            try:
                # Save raw audio (webm)
                with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp:
                    tmp.write(audio["bytes"])
                    webm_path = tmp.name

                # Convert to wav
                sound = AudioSegment.from_file(webm_path)
                wav_path = webm_path.replace(".webm", ".wav")
                sound.export(wav_path, format="wav")

                # Read wav
                with sr.AudioFile(wav_path) as source:
                    audio_data = recognizer.record(source)

                voice_text = recognizer.recognize_google(audio_data)

                st.success(f"🗣 Detected: {voice_text}")

            except sr.UnknownValueError:
                st.error("❌ Could not understand audio")

            except sr.RequestError:
                st.error("🌐 API unavailable (check internet)")

            except Exception as e:
                st.error(f"❌ Speech error: {e}")

        # ---------- FINAL TEXT ----------
        final_text = text_input.strip()

        if voice_text:
            final_text = voice_text

        # ---------- SHOW TEXT ----------
        if final_text:
            st.success(f"🗣 You said: {final_text}")

        # ---------- PROCESS ----------
        if final_text:

            words = final_text.lower().strip().split()

            st.markdown("<h3>🖐 Sign Output</h3>", unsafe_allow_html=True)

            # ---------- LOAD AVATARS ----------
            avatar_files = os.listdir("avatars") if os.path.exists("avatars") else []
            avatar_map = {}

            for file in avatar_files:
                name = file.replace(".gif", "")
                avatar_map[name] = f"avatars/{file}"

            matched = []

            # ---------- MATCH ----------
            full = "_".join(words)

            if full in avatar_map:
                matched.append((avatar_map[full], full))
            else:
                for word in words:
                    found = False

                    for key in avatar_map:
                        if word in key:
                            matched.append((avatar_map[key], key))
                            found = True
                            break

                    if not found:
                        matched.append((None, word))

            # ---------- DISPLAY ----------
            cols = st.columns(min(len(matched), 5))

            for i, (path, label) in enumerate(matched):

                with cols[i % len(cols)]:

                    st.markdown("""
                    <div class='custom-card' style='padding:15px; text-align:center;'>
                    """, unsafe_allow_html=True)

                    if path and os.path.exists(path):
                        play_gif(path, width=250)
                        st.caption(f"✅ {label}")
                    else:
                        st.warning(f"No avatar for '{label}'")

                    st.markdown("</div>", unsafe_allow_html=True)

    # ---------- BOTTOM ----------
    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("⬅ Back to Dashboard", use_container_width=True):
        st.session_state.page = "user_dashboard"
# ---------- ROUTER ----------
if "page" not in st.session_state:
    st.session_state.page = "home"

page = st.session_state.page

if page == "home":
    home()
elif page == "admin_login":
    admin_login()
elif page == "admin_dashboard":
    admin_dashboard()
elif page == "register":
    register()
elif page == "user_login":
    user_login()
elif page == "user_dashboard":
    user_dashboard()
elif page == "train_model":
    train_model_page()
    
elif page == "sign_to_voice":
    sign_to_voice_page()

elif page == "add_avatar":
    add_avatar_page()

elif page == "voice_to_sign":
    voice_to_sign_page()
