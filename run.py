"""
Entry point to run the Streamlit application.

This script imports the `chat` function from the `app.chat`
module and runs it when executed as the main program.
"""
from app.chat import chat

if __name__ == '__main__':
    chat()
