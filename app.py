import streamlit as st
from deepface import DeepFace
import numpy as np
from PIL import Image
import tempfile

# -----------------------------------
# CONFIG
# -----------------------------------
st.set_page_config(page_title="Face Authentication", layout="centered")

ADMIN_NAME = "Aarsh"
THRESHOLD = 0.40

st.markdown(
    "<h1 style='text-align:center;'>🌐 Face Authentication</h1>",
    unsafe_allow_html=True
)

# -----------------------------------
# SESSION STORAGE (In-Memory DB)
# -----------------------------------
if "authenticated_user" not in st.session_state:
    st.session_state.authenticated_user = None

if "users_db" not in st.session_state:
    st.session_state.users_db = {}  # {username: embedding}

# -----------------------------------
# FUNCTION: GET EMBEDDING
# -----------------------------------
def get_embedding(image):

    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        image.save(tmp.name)

        embedding = DeepFace.represent(
            img_path=tmp.name,
            model_name="Facenet",
            detector_backend="opencv",
            enforce_detection=False
        )[0]["embedding"]

    return np.array(embedding)


# -----------------------------------
# AUTHENTICATION
# -----------------------------------

if st.session_state.authenticated_user is None:

    st.subheader("🔎 Face Authentication")

    camera_img = st.camera_input("Take a picture to authenticate")

    if camera_img is not None:

        image = Image.open(camera_img)

        with st.spinner("Processing..."):
            live_embedding = get_embedding(image)

            best_user = None
            min_distance = 1.0

            for username, user_embedding in st.session_state.users_db.items():

                similarity = np.dot(live_embedding, user_embedding) / (
                    np.linalg.norm(live_embedding) * np.linalg.norm(user_embedding)
                )

                distance = 1 - similarity

                if distance < min_distance:
                    min_distance = distance
                    best_user = username

        if best_user and min_distance < THRESHOLD:

            confidence = round((1 - min_distance) * 100, 2)
            st.session_state.authenticated_user = best_user
            st.rerun()

        else:
            st.error("❌ Face Not Recognized")

# -----------------------------------
# DASHBOARD
# -----------------------------------

if st.session_state.authenticated_user is not None:

    st.success(f"Logged in as {st.session_state.authenticated_user}")

    if st.button("Logout"):
        st.session_state.authenticated_user = None
        st.rerun()

# -----------------------------------
# ADMIN PANEL
# -----------------------------------
st.markdown("---")
st.subheader("👥 Admin Panel")

if st.session_state.authenticated_user == ADMIN_NAME or len(st.session_state.users_db) == 0:

    # ADD USER
    st.markdown("### ➕ Register New User")

    new_user = st.text_input("Enter Username")

    register_img = st.camera_input("Capture Face for Registration", key="register")

    if register_img is not None and new_user:

        image = Image.open(register_img)

        with st.spinner("Generating embedding..."):
            embedding = get_embedding(image)

            st.session_state.users_db[new_user] = embedding

        st.success(f"User {new_user} registered successfully!")

    st.markdown("---")

    # DELETE USER
    if st.session_state.users_db:

        selected_user = st.selectbox(
            "Select User to Delete",
            list(st.session_state.users_db.keys())
        )

        if st.button("❌ Delete User"):
            del st.session_state.users_db[selected_user]
            st.success("User deleted.")
            st.rerun()

else:
    st.info("Login as Admin to manage users.")