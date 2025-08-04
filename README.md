# RAG Chatbot Backend

This repository contains the backend for a Retrieval-Augmented Generation (RAG) chatbot. The backend is built using FastAPI and integrates with FAISS for efficient vector search.

## Features
- User authentication
- Database integration
- FAISS vector index for semantic search
- RESTful API endpoints

## Directory Structure
```
backend/
  app/
    __init__.py
    auth.py
    db.py
    main.py
    schemas.py
  faiss_index/
    index.faiss
    index.pkl
  requirements.txt
```

## Installation

### Prerequisites
- Python 3.10 or higher
- Git
- (Recommended) Virtual environment tool (venv)

### Step 1: Clone the Repository
```powershell
git clone <repo-url>
cd backend
```

### Step 2: Create and Activate Virtual Environment
```powershell
python -m venv ragvenv
ragvenv\Scripts\activate
```

### Step 3: Install Dependencies
```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Prepare FAISS Index
- Place your FAISS index files (`index.faiss`, `index.pkl`) in the `faiss_index/` directory.
- If you need to generate a new index, refer to the documentation in `faiss_index/` or use your own data pipeline.

### Step 5: Run the Backend Server
```powershell
uvicorn app.main:app --reload
```

The server will start at `http://127.0.0.1:8000`.

## API Endpoints
See `endpoints.md` for a full list of available endpoints and their usage.

## Development
- All backend code is in the `app/` directory.
- Update `requirements.txt` when adding new dependencies.
- Use virtual environments to avoid dependency conflicts.

## Troubleshooting
- If you encounter issues with FAISS, ensure you have the correct version installed and compatible with your Python environment.
- For database errors, check your connection settings in `db.py`.

## License
MIT License

## Contact
For questions or support, please contact the repository owner.
