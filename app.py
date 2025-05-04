import streamlit as st
import requests

# Set page configuration
st.set_page_config(
    page_title="Thiel VC Assistant",
    page_icon="🦄",
    layout="centered"
)

# Add custom CSS for better styling
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .stTextInput>div>div>input {
        font-size: 16px;
        border-radius: 20px;
        padding: 10px 20px;
    }
    .stButton>button {
        width: 100%;
        background-color: #1E88E5;
        color: white;
        padding: 10px;
        border: none;
        border-radius: 20px;
        cursor: pointer;
        font-weight: 500;
    }
    .stButton>button:hover {
        background-color: #1565C0;
    }
    .welcome-box {
        background-color: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
    }
    .assistant-message {
        background-color: #E3F2FD;
        padding: 1rem;
        border-radius: 15px;
        margin: 1rem 0;
    }
    .user-message {
        background-color: #F5F5F5;
        padding: 1rem;
        border-radius: 15px;
        margin: 1rem 0;
    }
    .task-list {
        margin-top: 1rem;
        padding: 1rem;
        background-color: #F8F9FA;
        border-radius: 10px;
    }
    .task-item {
        display: flex;
        align-items: center;
        margin: 0.5rem 0;
        padding: 0.5rem;
        border-radius: 8px;
        background-color: white;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    .task-icon {
        margin-right: 10px;
        font-size: 1.2rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Title and welcome message
st.title("🦄 Thiel VC Assistant")

# Layout: LHS menu, RHS chat
col1, col2 = st.columns([2, 3], gap="large")

# Welcome box with task options
st.markdown("""
    <div class="welcome-box">
        <h2 style='text-align: center; color: #1E88E5;'>Welcome!</h2>
        <p style='text-align: center; font-size: 1.2rem;'>
            I'm Peter Thiel, your VC Assistant. How can I help you today?
        </p>
        <div class="task-list">
            <h3 style='color: #1E88E5; margin-bottom: 1rem;'>I can help you with:</h3>
            <div class="task-item">
                <span class="task-icon">📅</span>
                <span>Send a calendar invite!</span>
            </div>
            <div class="task-item">
                <span class="task-icon">✉️</span>
                <span>Send an email!</span>
            </div>
            <div class="task-item">
                <span class="task-icon">📝</span>
                <span>Create a memo on a company you are evaluating!</span>
            </div>
            <div class="task-item">
                <span class="task-icon">📰</span>
                <span>Get latest VC news!</span>
            </div>
            <div class="task-item">
                <span class="task-icon">🤖</span>
                <span>Get Hacker News feedback on the AI tool you like!</span>
            </div>
            <div class="task-item">
                <span class="task-icon">📁</span>
                <span>Work with your GDrive!</span>
            </div>
            <div class="task-item">
                <span class="task-icon">🔍</span>
                <span>Search your Affinity!</span>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Initialize chat history in session state if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "I'm Peter Thiel, your VC Assistant. How can I help you today?"}
    ]

# Display chat history
for message in st.session_state.messages:
    if message["role"] == "assistant":
        st.markdown(f"""
            <div class="assistant-message">
                <strong>Peter Thiel VC Assistant:</strong><br>
                {message["content"]}
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div class="user-message">
                <strong>You:</strong><br>
                {message["content"]}
            </div>
        """, unsafe_allow_html=True)

# Chat input with new placeholder
if prompt := st.chat_input("Let's get started!"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    st.markdown(f"""
        <div class="user-message">
            <strong>You:</strong><br>
            {prompt}
        </div>
    """, unsafe_allow_html=True)
    
    # Show a spinner while getting the response
    with st.spinner("Thinking..."):
        try:
            # Make API call using the exact format from the example
            API_URL = "https://ea-to-a-vc.onrender.com/api/v1/prediction/a1d7409d-89c8-4d85-ac32-101c1155c566"
            
            def query(payload):
                response = requests.post(API_URL, json=payload)
                return response.json()
            
            # Call the API with the user's message
            response_data = query({
                "question": prompt
            })
            
            # Extract the response text
            ai_response = response_data.get("text", "Sorry, I couldn't process that request.")
            
            # Add AI response to chat history
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
            
            # Display AI response
            st.markdown(f"""
                <div class="assistant-message">
                    <strong>Peter Thiel VC Assistant:</strong><br>
                    {ai_response}
                </div>
            """, unsafe_allow_html=True)
                
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.session_state.messages.append({"role": "assistant", "content": "Sorry, there was an error processing your request."})

# Add footer note
st.markdown("""
    <div style='text-align:center; color: #888; font-size: 0.95rem; margin-top: 2.5rem;'>
        Made by Astha - For Personal Use Only
    </div>
""", unsafe_allow_html=True) 