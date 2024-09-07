import streamlit as st
import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Function to generate content using Google Gemini API via HTTP request
def generate_content_gemini(api_key, prompt):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"
    headers = {
        "Content-Type": "application/json",
    }
    params = {
        'key': api_key
    }
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }
    response = requests.post(url, headers=headers, json=data, params=params)
    response.raise_for_status()  # Will raise an error for bad responses
    response_json = response.json()

    # Print the response for debugging
    st.write("API Response:", response_json)
    
    # Extract the content and handle it as normal text
    try:
        text = response_json.get('contents', [{}])[0].get('parts', [{}])[0].get('text', 'No text found')
        return text
    except KeyError as e:
        st.error(f"KeyError: {e}")
        return "Error: Unexpected response format."

# Streamlit app setup
st.title("Copilot")
st.write("This AI copilot code analyzes .")

# Load API key from .env file

api_key="AIzaSyBPDTMCefQxzW2q9JqzxKEck55-HcCBQpw"



if api_key:
    # Input text for the copilot
    user_input = st.text_area("Enter your code here:")

    # Button to trigger the analysis
    if st.button("Analyze Code"):
        if user_input:
            try:
                # Split the input into lines and find the middle line
                lines = user_input.split('\n')
                total_lines = len(lines)
                current_line = total_lines // 2  # Assuming the cursor is in the middle
                
                # Extract the previous 5 lines, current line, and next 5 lines
                start_line = max(current_line - 5, 0)
                end_line = min(current_line + 6, total_lines)  # Add 1 to include the current line
                code_context = "\n".join(lines[start_line:end_line])
                
                # Create a prompt with the extracted code context
                prompt = f"Analyze the following code context and provide suggestions:\n\n{code_context}"
                
                # Generate the content using Google Gemini
                content = generate_content_gemini(api_key, prompt)
                
                # Display the generated content as normal text
                st.subheader("Analysis Result:")
                st.write(content)
            except requests.exceptions.HTTPError as err:
                st.error(f"Error: {err}")
        else:
            st.write("Please enter your code.")
else:
    st.write("API Key is missing. Please check your .env file.")

# Add a sidebar for additional features (optional)
st.sidebar.title("Additional Features")
st.sidebar.write("You can extend this copilot with more features like content analysis, documentation generation, etc.")
