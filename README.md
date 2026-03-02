# Face Authentication System

A real-time face authentication system built using Python, Streamlit, OpenCV, and DeepFace.  
The application enables secure face-based login and includes an admin panel for managing users.

---

## Features

- Real-time face verification using webcam
- DeepFace with FaceNet model
- Confidence score calculation
- Admin panel to add, update, and delete users
- Adjustable authentication threshold
- Session-based login management

---

## Tech Stack

- Python
- Streamlit
- OpenCV
- DeepFace
- TensorFlow
- NumPy
- Pillow

---

## Project Structure

```
face-authentication-system/
│
├── app.py
├── register.py
├── users/
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Installation

### Clone the repository

```bash
git clone https://github.com/your-username/face-authentication-system.git
cd face-authentication-system
```

### Create virtual environment (recommended)

```bash
python -m venv face_env
face_env\Scripts\activate     # Windows
# source face_env/bin/activate  # Mac/Linux
```

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## Run the Application

```bash
streamlit run app.py
```

---

## Admin Access

Default Admin Name:
```
Aarsh
```

Admin users can:
- Add new users
- Update face data
- Delete users

---

## Face Registration (CLI)

```bash
python register.py
```

This captures and stores face images inside:
```
users/<username>/
```

---

## How It Works

1. Captures live image from webcam.
2. Compares with stored user images using DeepFace.
3. Uses FaceNet embeddings to compute similarity distance.
4. If distance is below the defined threshold, authentication succeeds.
5. Confidence is calculated as:

```
confidence = (1 - distance) * 100
```

Threshold can be modified in `app.py`:

```python
THRESHOLD = 0.35
```

---

## Future Improvements

- Liveness detection
- Embedding storage for faster matching
- Database integration
- Cloud deployment
- Multi-factor authentication

---

## Author

Aarsh Khadgi
