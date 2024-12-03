@echo off
setlocal enabledelayedexpansion

REM Check if virtual environment exists
if not exist "venv" (
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate

REM Install dependencies
pip install -r requirements.txt

REM Pull Ollama model
ollama pull llama3.2

REM Run Streamlit application
streamlit run src\app.py
