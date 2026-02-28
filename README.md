# Face Authentication System

A Streamlit-based face authentication system using DeepFace (FaceNet model) and cosine similarity. The application is fully compatible with Streamlit Cloud and uses browser-based camera input.

## Features

- Browser camera authentication
- Face recognition using FaceNet
- Cosine similarity matching
- Confidence score display
- Admin-based user registration
- In-memory embedding storage
- Streamlit Cloud compatible

## Technology Stack

- Python
- Streamlit
- DeepFace (FaceNet)
- NumPy
- Pillow

## Installation (Local Setup)

1. Clone the repository:
   git clone https://github.com/your-username/your-repo-name.git

2. Navigate to the project directory:
   cd your-repo-name

3. Install dependencies:
   pip install -r requirements.txt

4. Run the application:
   streamlit run app.py

## Deployment (Streamlit Cloud)

1. Push the project to GitHub.
2. Go to https://streamlit.io/cloud
3. Connect your repository.
4. Select `app.py` as the entry file.
5. Deploy.

## Important Notes

- User data is stored in session memory.
- All registered users are cleared when the app restarts.
- For production use, integrate a persistent database (e.g., Firebase, PostgreSQL, MongoDB).

## Project Structure

FaceAuthApp/
│
├── app.py  
├── requirements.txt  
└── README.md  

## License

This project is intended for academic and demonstration purposes.
