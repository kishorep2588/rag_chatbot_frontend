import streamlit as st
import requests

st.set_page_config(page_title="RAG App", layout="wide")
st.title("RAG App")

API_URL = "http://127.0.0.1:8000"

def show_header(title, icon):
    st.markdown(f"<h2 style='display:flex;align-items:center'>{icon} {title}</h2>", unsafe_allow_html=True)

def login():
    show_header("Login", "🔑")
    username = st.text_input("Username", help="Enter your username")
    password = st.text_input("Password", type="password", help="Enter your password")
    if st.button("Login", use_container_width=True):
        response = requests.post(f"{API_URL}/login", json={"username": username, "password": password})
        if response.status_code == 200:
            token = response.json()["access_token"]
            st.session_state["token"] = token
            st.write(token)
            st.success("Logged in! 🎉")
        else:
            st.error(response.json().get("detail", "Login failed"))

def register():
    show_header("Register (Admin Only)", "📝")
    username = st.text_input("Username", help="Enter your username")
    password = st.text_input("Password", type="password", help="Enter your password")
    email = st.text_input("Email", help="Enter your email")
    role = st.selectbox("Role", ["user", "admin"], help="Select your role")
    if st.button("Register", use_container_width=True):
        response = requests.post(f"{API_URL}/register", json={
            "username": username,
            "password": password,
            "email": email,
            "role": role
        })
        if response.status_code == 200:
            st.success("User registered successfully! 🎉")
        else:
            st.error(response.json().get("detail", "Registration failed"))

def upload_pdfs():
    show_header("Upload PDFs", "📄")
    if "token" not in st.session_state:
        st.error("Please log in first.")
        return

    uploaded_files = st.file_uploader("Upload PDF files", type=["pdf"], accept_multiple_files=True)
    if st.button("Upload", use_container_width=True):
        if not uploaded_files:
            st.error("Please upload at least one PDF file.")
            return
        headers = {"Authorization": f"Bearer {st.session_state['token']}"}
        files = [("files", (file.name, file, "application/pdf")) for file in uploaded_files]
        response = requests.post(f"{API_URL}/upload_file", files=files, headers=headers)
        if response.status_code == 200:
            st.success("Uploaded all files successfully! 🎉")
            results = response.json()['results']
            filenames = [result['filename'] for result in results]
            st.session_state['filenames'] = filenames
            st.write(filenames)
        else:
            st.error(response.json().get("detail", "Failed to upload files"))

def generate_embeddings():
    show_header("Generate Embeddings", "🧠")
    if "token" not in st.session_state:
        st.error("Please log in first.")
        return

    if st.button("Generate Embeddings", use_container_width=True):
        headers = {"Authorization": f"Bearer {st.session_state['token']}"}
        filenames = st.session_state.get('filenames', [])
        if not filenames:
            st.error("No files uploaded. Please upload PDFs first.")
            return
        response = requests.post(f"{API_URL}/generate_embeddings", headers=headers, json=filenames)
        if response.status_code == 200:
            st.success("Generated embeddings successfully! 🎉")
            st.write(response.json())
        else:
            st.error(response.json().get("detail", "Failed to generate embeddings"))

def query():
    show_header("Query", "💬")
    if "token" not in st.session_state:
        st.error("Please log in first.")
        return

    query_text = st.text_input("Enter your query", help="Type your question here")
    if st.button("Submit Query", use_container_width=True):
        headers = {"Authorization": f"Bearer {st.session_state['token']}"}
        response = requests.post(f"{API_URL}/query", headers=headers, json=query_text)
        if response.status_code == 200:
            st.write(response.json())
        else:
            st.error(response.json().get("detail", "Failed to get query results"))


st.sidebar.image("https://img.icons8.com/color/96/000000/robot.png", width=64)
st.sidebar.title("RAG Chatbot")
page = st.sidebar.radio("Go to", [

    "Login", "Register", "Upload PDFs", "Generate Embeddings", "Query"
], format_func=lambda x: {
    "Login": "🔑 Login",
    "Register": "📝 Register",
    "Upload PDFs": "📄 Upload PDFs",
    "Generate Embeddings": "🧠 Generate Embeddings",
    "Query": "💬 Query"
}[x])

st.markdown(
    """
    <style>

    .stButton>button {font-size: 18px;}
    .stTextInput>div>input {font-size: 16px;}
    .stTextArea>div>textarea {font-size: 16px;}

    </style>
    """, unsafe_allow_html=True
)


if page == "Login":
    login()
elif page == "Register":
    register()
elif page == "Upload PDFs":
    upload_pdfs()
elif page == "Generate Embeddings":
    generate_embeddings()
elif page == "Query":
    query()