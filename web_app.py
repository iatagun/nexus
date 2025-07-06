"""
Streamlit Web Interface for Nexus AI Assistant
"""

import streamlit as st
import sys
import os
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

try:
    from nexus import AIAssistant
except ImportError as e:
    st.error(f"Import error: {e}")
    st.error("Please make sure the nexus package is properly installed.")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="Nexus AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
.main-header {
    text-align: center;
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 2.5rem;
    font-weight: bold;
    margin-bottom: 1rem;
}

.chat-message {
    padding: 1rem;
    border-radius: 0.5rem;
    margin: 0.5rem 0;
    border-left: 4px solid;
}

.user-message {
    background-color: #f0f2f6;
    border-left-color: #667eea;
}

.assistant-message {
    background-color: #e8f4fd;
    border-left-color: #764ba2;
}
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables"""
    if "assistant" not in st.session_state:
        try:
            st.session_state.assistant = AIAssistant()
            st.session_state.conversation_history = []
            st.session_state.is_initialized = True
            st.session_state.model_provider = st.session_state.assistant.model_provider
            st.session_state.model_name = st.session_state.assistant.model_name
        except Exception as e:
            st.session_state.is_initialized = False
            st.session_state.error_message = str(e)


def display_chat_message(role: str, content: str):
    """Display a chat message with proper styling"""
    if role == "user":
        st.markdown(f"""
        <div class="chat-message user-message">
            <strong>👤 You:</strong><br>
            {content}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-message assistant-message">
            <strong>🤖 Nexus:</strong><br>
            {content}
        </div>
        """, unsafe_allow_html=True)


def main():
    """Main Streamlit application"""
    
    # Initialize session state
    initialize_session_state()
    
    # Header
    st.markdown('<h1 class="main-header">🤖 Nexus AI Assistant</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Check if assistant is initialized
        if not st.session_state.get("is_initialized", False):
            st.error("❌ Failed to initialize AI Assistant")
            if "error_message" in st.session_state:
                st.error(f"Error: {st.session_state.error_message}")
            st.stop()
        
        st.success("✅ AI Assistant Ready")
        
        # Show current model info
        if hasattr(st.session_state, 'model_provider'):
            st.info(f"🤖 Provider: {st.session_state.model_provider}")
            st.info(f"📋 Model: {st.session_state.model_name}")
        
        # Conversation controls
        if st.button("🔄 Reset Conversation"):
            st.session_state.assistant.reset_conversation()
            st.session_state.conversation_history = []
            st.success("Conversation reset!")
            st.rerun()
        
        # Model settings
        st.subheader("🔧 Model Settings")
        temperature = st.slider("Temperature", 0.0, 2.0, 0.7, 0.1)
        max_tokens = st.slider("Max Tokens", 100, 4000, 2000, 100)
        
        # Statistics
        st.subheader("📊 Statistics")
        st.metric("Messages in History", len(st.session_state.conversation_history))
    
    # Main chat interface
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("💬 Chat with Nexus")
        
        # Display conversation history
        chat_container = st.container()
        
        with chat_container:
            for message in st.session_state.conversation_history:
                display_chat_message(message["role"], message["content"])
        
        # Chat input
        with st.form("chat_form", clear_on_submit=True):
            user_input = st.text_area(
                "Your message:",
                placeholder="Ask me anything...",
                height=100,
                key="user_input"
            )
            
            col_send, col_example = st.columns([1, 2])
            
            with col_send:
                send_button = st.form_submit_button("🚀 Send", use_container_width=True)
            
            with col_example:
                if st.form_submit_button("💡 Example Question", use_container_width=True):
                    user_input = "What can you help me with?"
                    send_button = True
        
        # Process user input
        if send_button and user_input.strip():
            # Add user message to history
            st.session_state.conversation_history.append({
                "role": "user",
                "content": user_input
            })
            
            # Show thinking spinner
            with st.spinner("🤔 Nexus is thinking..."):
                try:
                    # Get response from assistant
                    response = st.session_state.assistant.ask(
                        user_input,
                        temperature=temperature,
                        max_tokens=max_tokens
                    )
                    
                    # Add assistant response to history
                    st.session_state.conversation_history.append({
                        "role": "assistant",
                        "content": response
                    })
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
            
            # Rerun to update the chat display
            st.rerun()
    
    with col2:
        st.subheader("🎯 Quick Actions")
        
        # Predefined prompts
        quick_prompts = [
            "Explain quantum computing",
            "Write a Python function",
            "Help me debug code",
            "Create a meal plan",
            "Explain machine learning",
            "Write a poem",
            "Solve a math problem"
        ]
        
        for prompt in quick_prompts:
            if st.button(f"💭 {prompt}", use_container_width=True):
                # Add this prompt to conversation
                st.session_state.conversation_history.append({
                    "role": "user", 
                    "content": prompt
                })
                
                # Get AI response
                with st.spinner("🤔 Nexus is thinking..."):
                    try:
                        response = st.session_state.assistant.ask(prompt)
                        st.session_state.conversation_history.append({
                            "role": "assistant",
                            "content": response
                        })
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
                
                st.rerun()
        
        st.markdown("---")
        
        # About section
        st.subheader("ℹ️ About Nexus")
        st.markdown("""
        Nexus is an intelligent AI assistant designed to help you with:
        
        - 🧠 **Answering Questions**
        - 💻 **Coding Assistance** 
        - 🎨 **Creative Writing**
        - 📊 **Data Analysis**
        - 🔧 **Problem Solving**
        
        Built with ❤️ using Streamlit and OpenAI.
        """)


if __name__ == "__main__":
    main()
