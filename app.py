import streamlit as st # type: ignore
import cv2
from deepface import DeepFace # type: ignore
import os

# -----------------------------------
# CONFIG
# -----------------------------------
st.set_page_config(page_title="Face Unlock", layout="centered")

ADMIN_NAME = "Aarsh"
THRESHOLD = 0.35   # Tune between 0.35 - 0.45 if needed

st.markdown(
    "<h1 style='text-align:center;'>🔐 Face Authentication System</h1>",
    unsafe_allow_html=True
)

# -----------------------------------
# SESSION
# -----------------------------------
if "authenticated_user" not in st.session_state:
    st.session_state.authenticated_user = None

if not os.path.exists("users"):
    os.makedirs("users")

# -----------------------------------
# AUTHENTICATION
# -----------------------------------
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🔎 Face Authentication")
    authenticate = st.button("Authenticate")

if authenticate:

    user_folders = [
        u for u in os.listdir("users")
        if os.path.isdir(os.path.join("users", u))
    ]

    if not user_folders:
        st.warning("No users registered.")
        st.stop()

    cam = cv2.VideoCapture(0)

    with col_right:
        frame_placeholder = st.empty()
        st.info("📷 Camera started. Please look at the camera...")

        try:
            for _ in range(60):
                ret, frame = cam.read()
                if not ret:
                    st.error("Camera error.")
                    st.stop()

                frame = cv2.resize(frame, (440, 300))
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_placeholder.image(frame_rgb, channels="RGB")

            ret, frame = cam.read()
            if not ret:
                st.error("Capture failed.")
                st.stop()

            frame = cv2.resize(frame, (640, 480))
            cv2.imwrite("live.jpg", frame)

        finally:
            cam.release()

        with st.spinner("🔎 Verifying..."):

            matched_user = None

            for user in user_folders:

                user_path = os.path.join("users", user)

                for img_file in os.listdir(user_path):

                    img_path = os.path.join(user_path, img_file)

                    try:
                        result = DeepFace.verify(
                            img1_path=img_path,
                            img2_path="live.jpg",
                            model_name="Facenet",
                            detector_backend="opencv",
                            enforce_detection=False
                        )

                        if result["verified"] and result["distance"] < THRESHOLD:
                            matched_user = user
                            break

                    except:
                        continue

                if matched_user:
                    break

    if matched_user:
        st.session_state.authenticated_user = matched_user

        # Convert distance to confidence %
        confidence = round((1 - result["distance"]) * 100, 2)

        colA, colB = st.columns(2)

        with colA:
            st.success(f"✅ Welcome {matched_user}")

        with colB:
            st.info(f"Confidence: {confidence}%")

    else:
        st.error("❌ Face Not Recognized")
# -----------------------------------
# DASHBOARD
# -----------------------------------
if st.session_state.authenticated_user:
    st.markdown("---")
    st.success(f"Logged in as {st.session_state.authenticated_user}")

    if st.button("Logout"):
        st.session_state.authenticated_user = None
        st.rerun()

# -----------------------------------
# ADMIN PANEL
# -----------------------------------
st.markdown("---")
st.subheader("👥 Admin Panel")

if st.session_state.authenticated_user == ADMIN_NAME:

    # -----------------------------------
    # ADD USER
    # -----------------------------------
    st.markdown("### ➕ Add New User")

    colC, colD = st.columns(2)

    with colC:
        new_user = st.text_input("Enter User Name")
        capture_clicked = st.button("Capture & Add Images")

    if capture_clicked:

        if new_user.strip() == "":
            st.error("Enter valid name.")
            st.stop()

        user_folder = os.path.join("users", new_user)

        if not os.path.exists(user_folder):
            os.makedirs(user_folder)

        cam = cv2.VideoCapture(0)

        with colD:
            frame_placeholder = st.empty()
            st.info("📷 Capturing 5 images...")

            try:
                for i in range(5):
                    for _ in range(30):
                        ret, frame = cam.read()
                        if not ret:
                            st.stop()

                        frame = cv2.resize(frame, (440, 300))
                        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        frame_placeholder.image(frame_rgb, channels="RGB")

                    cv2.imwrite(f"{user_folder}/img_{i}.jpg", frame)

                st.success(f"✅ Images captured for {new_user}")

            finally:
                cam.release()

    st.markdown("---")

    # -----------------------------------
    # DELETE / UPDATE
    # -----------------------------------
    user_folders = [
        u for u in os.listdir("users")
        if os.path.isdir(os.path.join("users", u))
    ]

    if user_folders:

        selected_user = st.selectbox("Select User", user_folders)

        col1, col2 = st.columns(2)

        # DELETE
        if col1.button("❌ Delete User"):
            user_path = os.path.join("users", selected_user)

            for file in os.listdir(user_path):
                os.remove(os.path.join(user_path, file))

            os.rmdir(user_path)
            st.success("User deleted.")
            st.rerun()

        # UPDATE
        if col2.button("🔄 Update Face"):

            user_folder = os.path.join("users", selected_user)

            cam = cv2.VideoCapture(0)

            preview_left, preview_right = st.columns(2)

            with preview_right:
                frame_placeholder = st.empty()
                st.info("📷 Updating face (5 new images)...")

                try:
                    for i in range(5):
                        for _ in range(30):
                            ret, frame = cam.read()
                            if not ret:
                                st.stop()

                            frame = cv2.resize(frame, (440, 300))
                            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                            frame_placeholder.image(frame_rgb, channels="RGB")

                        cv2.imwrite(f"{user_folder}/img_{i}.jpg", frame)

                    st.success("User face updated.")

                finally:
                    cam.release()

else:
    st.info("Login as Admin to manage users.")