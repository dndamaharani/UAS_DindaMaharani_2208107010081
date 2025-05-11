import streamlit as st
import requests
import json
from typing import List
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API configuration
API_URL = os.getenv("API_URL", "http://localhost:8000")

# App title and description
st.set_page_config(
    page_title="Intelligent Email Writer for Students",
    page_icon="📝",
    layout="centered"
)

# Title and introduction
st.title("📝 Intelligent Email Writer")
st.markdown("""
This application helps students generate professional emails using Gemini AI technology.
Fill in the details below, and we'll create a well-structured email for you.
""")

# Sidebar with information
with st.sidebar:
    st.header("About")
    st.markdown("""
    **Intelligent Email Writer** helps students create professional emails quickly and efficiently.
    
    Powered by Google's Gemini API, this tool generates high-quality emails based on your input.
    
    **How to use:**
    1. Select email category and tone
    2. Choose your preferred language
    3. Enter recipient, subject, and key points
    4. Click "Generate Email"
    """)
    
    st.divider()
    
    st.markdown("**Developed by:**")
    st.markdown("Alfi Zamriza | [GitHub](https://github.com/alfizamriza)")

# Create a form for email generation
with st.form("email_form"):
    # Email category
    category = st.selectbox(
        "Email Category",
        ["Academic", "Thesis", "Internship", "General"],
        index=0
    )
    
    # Two columns for tone and language
    col1, col2 = st.columns(2)
    
    with col1:
        tone = st.selectbox(
            "Tone",
            ["Formal", "Neutral", "Casual"],
            index=0
        )
    
    with col2:
        language = st.selectbox(
            "Language",
            ["English", "Indonesian"],
            index=0
        )
    
    # Recipient and subject
    recipient = st.text_input("Recipient (Name/Email)")
    subject = st.text_input("Subject")
    
    # Key points (dynamic list)
    st.subheader("Key Points")
    st.markdown("Add the main points you want to include in your email")
    
    # Initialize key_points in session state if not present
    if 'key_points' not in st.session_state:
        st.session_state.key_points = [""]
    
    # Display key point fields
    updated_key_points = []
    for i, key_point in enumerate(st.session_state.key_points):
        col1, col2 = st.columns([5, 1])
        with col1:
            updated_value = st.text_area(f"Point {i+1}", value=key_point, key=f"point_{i}", height=50)
            updated_key_points.append(updated_value)
        with col2:
            if len(st.session_state.key_points) > 1:  # Only show remove option if there's more than one field
                remove = st.checkbox("Remove", key=f"remove_{i}")
                if remove:
                    st.session_state.key_points.pop(i)
                    st.rerun()
    
    # Update session state with potentially modified values
    st.session_state.key_points = updated_key_points
    
    # Button to add new key point (outside the form's immediate button logic)
    add_point = st.checkbox("Add Another Point", key="add_point")
    if add_point:
        st.session_state.key_points.append("")
        st.rerun()
    
    # Optional sender information
    st.subheader("Sender Information (Optional)")
    sender_name = st.text_input("Your Name")
    sender_position = st.text_input("Your Position/Role")
    
    # Generate button
    generate_button = st.form_submit_button("✉️ Generate Email")

# When the form is submitted
if generate_button:
    # Validate inputs
    if not recipient:
        st.error("Please enter a recipient.")
    elif not subject:
        st.error("Please enter a subject.")
    elif not any(point.strip() for point in st.session_state.key_points):
        st.error("Please add at least one key point.")
    else:
        # Filter out empty key points
        valid_key_points = [point for point in st.session_state.key_points if point.strip()]
        
        # Prepare data for API request
        data = {
            "category": category.lower(),
            "tone": tone.lower(),
            "language": language,
            "recipient": recipient,
            "subject": subject,
            "key_points": valid_key_points,
            "sender_name": sender_name if sender_name else None,
            "sender_position": sender_position if sender_position else None
        }
        
        # Show loading indicator
        with st.spinner("Generating your email..."):
            try:
                # Make request to backend API
                response = requests.post(f"{API_URL}/generate-email", json=data)
                
                if response.status_code == 200:
                    email_content = response.json()["email_content"]
                    
                    # Display the generated email
                    st.success("Email generated successfully!")
                    st.subheader("Generated Email")
                    
                    # Display in a nice format
                    st.markdown("---")
                    st.markdown(email_content)
                    st.markdown("---")
                    
                    # Add copy button
                    if st.button("📋 Copy to Clipboard"):
                        st.write("Email copied to clipboard!")
                        st.session_state.clipboard = email_content
                        st.toast("Email copied to clipboard!", icon="✅")
                        
                else:
                    st.error(f"Error: {response.json().get('detail', 'Unknown error occurred')}")
            
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.info("Make sure the backend server is running at " + API_URL)

# Footer
st.markdown("---")
st.markdown("📧 Intelligent Email Writer for Students | Powered by Google Gemini API")