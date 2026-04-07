# devlup-backend
Core backend for DevlUp Labs — powering the main website and all flagship programs including Winter of Code and Summer of Code.

## Setup & Installation

1. Create a Virtual Environment (if not already done) and activate it:
   ```bash
   python -m venv venv
   
   # On Windows:
   .\venv\Scripts\activate
   
   # On Mac/Linux:
   source venv/bin/activate
   ```

2. Install the required dependencies from the newly generated requirements file:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Server

Start the FastAPI application with Uvicorn in development mode. Make sure you are in the `devlup-backend` directory and your virtual environment is active:
```bash
uvicorn server.main:app --reload
```
