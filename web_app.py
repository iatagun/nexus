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

# Custom CSS - Mysterious & Minimal Theme
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* Global Styles */
.stApp {
    background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 50%, #16213e 100%);
    color: #e0e0e0;
    font-family: 'Inter', sans-serif;
}

/* Remove default padding */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Sidebar Styling */
.css-1d391kg {
    background: linear-gradient(180deg, #0f0f0f 0%, #1a1a2e 100%);
    border-right: 1px solid #333;
}

/* Main Header */
.main-header {
    text-align: center;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 2.8rem;
    font-weight: 700;
    margin-bottom: 2rem;
    letter-spacing: -0.02em;
    text-shadow: 0 0 20px rgba(102, 126, 234, 0.3);
}

/* Chat Messages */
.chat-message {
    padding: 1.5rem;
    border-radius: 1rem;
    margin: 1rem 0;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    position: relative;
    overflow: hidden;
}

.chat-message::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
    z-index: -1;
}

.user-message {
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.15), rgba(118, 75, 162, 0.1));
    border-left: 3px solid #667eea;
    box-shadow: 0 8px 32px rgba(102, 126, 234, 0.2);
}

.assistant-message {
    background: linear-gradient(135deg, rgba(118, 75, 162, 0.15), rgba(240, 147, 251, 0.1));
    border-left: 3px solid #764ba2;
    box-shadow: 0 8px 32px rgba(118, 75, 162, 0.2);
}

/* Input Styling */
.stTextArea textarea {
    background: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 0.5rem !important;
    color: #e0e0e0 !important;
    backdrop-filter: blur(10px);
}

.stTextArea textarea:focus {
    border-color: #667eea !important;
    box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2) !important;
}

/* Button Styling */
.stButton button {
    background: linear-gradient(135deg, #667eea, #764ba2) !important;
    border: none !important;
    border-radius: 0.5rem !important;
    color: white !important;
    font-weight: 500 !important;
    padding: 0.5rem 1rem !important;
    transition: all 0.3s ease !important;
}

.stButton button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3) !important;
}

/* Selectbox Styling */
.stSelectbox div[data-baseweb="select"] {
    background: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 0.5rem !important;
}

/* Slider Styling */
.stSlider .stSlider-thumb {
    background: linear-gradient(135deg, #667eea, #764ba2) !important;
}

/* Metrics */
.metric-container {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 0.5rem;
    padding: 1rem;
    margin: 0.5rem 0;
}

/* Success/Error Messages */
.stSuccess {
    background: linear-gradient(135deg, rgba(0, 255, 0, 0.1), rgba(0, 200, 0, 0.1)) !important;
    border: 1px solid rgba(0, 255, 0, 0.2) !important;
    border-radius: 0.5rem !important;
}

.stError {
    background: linear-gradient(135deg, rgba(255, 0, 0, 0.1), rgba(200, 0, 0, 0.1)) !important;
    border: 1px solid rgba(255, 0, 0, 0.2) !important;
    border-radius: 0.5rem !important;
}

/* Glowing Effect */
.glow {
    animation: glow 2s ease-in-out infinite alternate;
}

@keyframes glow {
    from { text-shadow: 0 0 10px rgba(102, 126, 234, 0.3); }
    to { text-shadow: 0 0 20px rgba(102, 126, 234, 0.6); }
}

/* Loading Animation */
.loading {
    display: inline-block;
    width: 20px;
    height: 20px;
    border: 3px solid rgba(102, 126, 234, 0.3);
    border-radius: 50%;
    border-top-color: #667eea;
    animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

/* Mysterious Particles Effect */
.particles {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: -1;
}

.particle {
    position: absolute;
    width: 2px;
    height: 2px;
    background: rgba(102, 126, 234, 0.3);
    border-radius: 50%;
    animation: float 6s ease-in-out infinite;
}

@keyframes float {
    0%, 100% { transform: translateY(0px) rotate(0deg); opacity: 0; }
    50% { transform: translateY(-20px) rotate(180deg); opacity: 1; }
}

/* Scrollbar Styling */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0.1);
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, #667eea, #764ba2);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(135deg, #764ba2, #667eea);
}
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables"""
    if "assistant" not in st.session_state:
        try:
            st.session_state.assistant = AIAssistant()
            st.session_state.is_initialized = True
            st.session_state.model_provider = st.session_state.assistant.model_provider
            st.session_state.model_name = st.session_state.assistant.model_name
        except Exception as e:
            st.session_state.is_initialized = False
            st.session_state.error_message = str(e)
    
    # Initialize multi-chat system
    if "chat_sessions" not in st.session_state:
        st.session_state.chat_sessions = {
            "chat_1": {
                "id": "chat_1",
                "name": "Chat 1",
                "history": [],
                "created_at": "2025-01-01 10:00:00",
                "last_updated": "2025-01-01 10:00:00"
            }
        }
    
    if "active_chat_id" not in st.session_state:
        st.session_state.active_chat_id = "chat_1"
    
    if "chat_counter" not in st.session_state:
        st.session_state.chat_counter = 1
    
    # Maintain backward compatibility
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = st.session_state.chat_sessions[st.session_state.active_chat_id]["history"]


def display_chat_message(role: str, content: str, message_index: int = None):
    """Display a chat message with mysterious styling and feedback options"""
    if role == "user":
        st.markdown(f"""
        <div class="chat-message user-message">
            <strong>✨ You:</strong><br>
            <div style="margin-top: 0.5rem; line-height: 1.6;">{content}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-message assistant-message">
            <strong>🔮 Nexus:</strong><br>
            <div style="margin-top: 0.5rem; line-height: 1.6;">{content}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Add feedback buttons for assistant messages
        if message_index is not None:
            feedback_col1, feedback_col2, feedback_col3, feedback_col4 = st.columns([1, 1, 1, 3])
            
            with feedback_col1:
                if st.button("👍", key=f"good_{message_index}", help="Good response"):
                    provide_message_feedback(message_index, 1)
            
            with feedback_col2:
                if st.button("👎", key=f"bad_{message_index}", help="Poor response"):
                    provide_message_feedback(message_index, -1)
            
            with feedback_col3:
                if st.button("🔄", key=f"regenerate_{message_index}", help="Regenerate response"):
                    regenerate_response(message_index)


def provide_message_feedback(message_index: int, rating: int):
    """Provide feedback for a specific message"""
    try:
        if message_index * 2 + 1 < len(st.session_state.conversation_history):
            user_msg = st.session_state.conversation_history[message_index * 2]['content']
            assistant_msg = st.session_state.conversation_history[message_index * 2 + 1]['content']
            
            result = st.session_state.assistant.provide_feedback(user_msg, assistant_msg, rating)
            
            feedback_text = "👍 Positive" if rating == 1 else "👎 Negative"
            st.success(f"{feedback_text} feedback recorded! Quality score: {result['overall_quality']:.2f}")
            
            if result['suggestions']:
                st.info("💡 Suggestions: " + ", ".join(result['suggestions'][:2]))
                
            st.rerun()
    except Exception as e:
        st.error(f"Error providing feedback: {e}")


def regenerate_response(message_index: int):
    """Regenerate the assistant's response"""
    try:
        if message_index * 2 < len(st.session_state.conversation_history):
            user_msg = st.session_state.conversation_history[message_index * 2]['content']
            
            # Remove the old assistant response
            if message_index * 2 + 1 < len(st.session_state.conversation_history):
                st.session_state.conversation_history.pop(message_index * 2 + 1)
            
            # Generate new response
            with st.spinner("🔄 Regenerating response..."):
                response = st.session_state.assistant.ask(user_msg)
                st.session_state.conversation_history.append({
                    "role": "assistant",
                    "content": response
                })
            
            st.rerun()
    except Exception as e:
        st.error(f"Error regenerating response: {e}")


def handle_learning_action(action_key: str):
    """Handle learning-related actions"""
    try:
        if action_key == "show_stats":
            if hasattr(st.session_state, 'assistant'):
                stats = st.session_state.assistant.get_learning_stats()
                st.info(f"""
                📊 **Learning Statistics**
                - Total conversations: {stats['total_conversations']}
                - Positive feedback: {stats['positive_feedback_rate']:.1%}
                - Quality score: {stats['avg_quality_score']:.1%}
                - Response time: {stats['avg_response_time']:.1f}s
                """)
        
        elif action_key == "show_improvement":
            if hasattr(st.session_state, 'assistant'):
                summary = st.session_state.assistant.continuous_improvement_summary()
                st.info(f"""
                🧠 **Improvement Status**
                - Level: {summary['improvement_level']}
                - Interactions: {summary['total_interactions']}
                - Satisfaction: {summary['satisfaction_rate']}
                - Quality: {summary['quality_score']}
                """)
        
        elif action_key == "reset_learning":
            if st.confirm("Are you sure you want to reset all learning data?"):
                # This would reset the learning database
                st.warning("🔄 Learning data reset functionality would be implemented here")
                
        elif action_key == "get_suggestions":
            if hasattr(st.session_state, 'assistant'):
                suggestions = st.session_state.assistant.suggest_improvements()
                st.info("💡 **Improvement Suggestions:**\n" + "\n".join([f"• {s}" for s in suggestions]))
                
    except Exception as e:
        st.error(f"Error handling learning action: {e}")


def main():
    """Main Streamlit application"""
    
    # Initialize session state
    initialize_session_state()
    
    # Mysterious Header with particles effect
    st.markdown("""
    <div class="particles">
        <div class="particle" style="left: 10%; animation-delay: 0s;"></div>
        <div class="particle" style="left: 20%; animation-delay: 0.5s;"></div>
        <div class="particle" style="left: 30%; animation-delay: 1s;"></div>
        <div class="particle" style="left: 40%; animation-delay: 1.5s;"></div>
        <div class="particle" style="left: 50%; animation-delay: 2s;"></div>
        <div class="particle" style="left: 60%; animation-delay: 2.5s;"></div>
        <div class="particle" style="left: 70%; animation-delay: 3s;"></div>
        <div class="particle" style="left: 80%; animation-delay: 3.5s;"></div>
        <div class="particle" style="left: 90%; animation-delay: 4s;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<h1 class="main-header glow">✨ NEXUS ✨</h1>', unsafe_allow_html=True)
    st.markdown('<div style="text-align: center; margin-bottom: 2rem; opacity: 0.7; font-size: 1.1rem;">◦ AI Assistant ◦</div>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown('<h2 style="text-align: center; margin-bottom: 1rem;">⚙️ Control Panel</h2>', unsafe_allow_html=True)
        
        # Check if assistant is initialized
        if not st.session_state.get("is_initialized", False):
            st.error("❌ Failed to initialize AI Assistant")
            if "error_message" in st.session_state:
                st.error(f"Error: {st.session_state.error_message}")
            st.stop()
        
        st.markdown('<div style="text-align: center; padding: 1rem; background: rgba(0, 255, 0, 0.1); border-radius: 0.5rem; margin-bottom: 1rem;">🟢 System Online</div>', unsafe_allow_html=True)
        
        # Show current model info
        if hasattr(st.session_state, 'model_provider'):
            st.markdown(f'<div class="metric-container">🤖 Provider: <strong>{st.session_state.model_provider}</strong></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-container">📋 Model: <strong>{st.session_state.model_name}</strong></div>', unsafe_allow_html=True)
        
        # Conversation controls
        if st.button("🔄 Reset Conversation"):
            st.session_state.assistant.reset_conversation()
            st.session_state.conversation_history = []
            st.success("Conversation reset!")
            st.rerun()
        
        # Model settings
        st.subheader("🔧 Model Settings")
        
        # Model selection for Ollama
        if st.session_state.get('model_provider') == 'ollama':
            try:
                import ollama
                models_response = ollama.list()
                model_names = [model['model'] for model in models_response['models']]
                
                if model_names:
                    current_model = os.getenv('OLLAMA_MODEL', 'deepseek-coder:latest')
                    selected_model = st.selectbox(
                        "Select Ollama Model:",
                        options=model_names,
                        index=model_names.index(current_model) if current_model in model_names else 0
                    )
                    
                    if selected_model != current_model:
                        if st.button("🔄 Switch Model"):
                            os.environ['OLLAMA_MODEL'] = selected_model
                            # Re-initialize assistant with new model
                            st.session_state.assistant = AIAssistant()
                            st.session_state.model_name = selected_model
                            st.success(f"Switched to {selected_model}")
                            st.rerun()
                else:
                    st.warning("No Ollama models found. Pull some models first.")
            except Exception as e:
                st.error(f"Error loading Ollama models: {e}")
                st.error(f"Debug info: {type(e).__name__}: {str(e)}")
        
        temperature = st.slider("Temperature", 0.0, 2.0, 0.7, 0.1)
        max_tokens = st.slider("Max Tokens", 100, 4000, 2000, 100)
        
        # Learning Statistics Section
        st.markdown('<div style="height: 1rem;"></div>', unsafe_allow_html=True)
        st.subheader("🧠 Learning Stats")
        
        try:
            if hasattr(st.session_state, 'assistant'):
                stats = st.session_state.assistant.get_learning_stats()
                
                # Display learning metrics
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Conversations", stats['total_conversations'])
                    st.metric("Quality Score", f"{stats['avg_quality_score']:.1%}")
                
                with col2:
                    st.metric("Positive Rate", f"{stats['positive_feedback_rate']:.1%}")
                    st.metric("Response Time", f"{stats['avg_response_time']:.1f}s")
                
                # Learning level
                if stats['total_conversations'] > 0:
                    summary = st.session_state.assistant.continuous_improvement_summary()
                    level = summary['improvement_level']
                    level_color = {
                        'Learning Phase': '🟡',
                        'Adapting': '🟠', 
                        'Well Adapted': '�',
                        'Highly Optimized': '🔥'
                    }.get(level, '🟡')
                    
                    st.markdown(f"""
                    <div class="metric-container" style="text-align: center;">
                        <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">{level_color}</div>
                        <div style="font-size: 0.9rem; opacity: 0.7;">Learning Level</div>
                        <div style="font-size: 1rem; font-weight: bold; margin-top: 0.5rem;">{level}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Show learned patterns
                    if stats['learned_patterns']:
                        st.markdown("**🔬 Learned Patterns:**")
                        for pattern_type, count in stats['learned_patterns'].items():
                            st.markdown(f"• {pattern_type}: {count}")
                else:
                    st.info("🌱 System is ready to learn from interactions")
                    
        except Exception as e:
            st.error(f"Learning stats unavailable: {e}")
        
        # Statistics
        st.subheader("📊 Session Stats")
        st.metric("Messages in History", len(st.session_state.conversation_history))
    
    # Main chat interface
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown('<h3 style="text-align: center; margin-bottom: 2rem; opacity: 0.8;">💫 Neural Interface</h3>', unsafe_allow_html=True)
        
        # Display conversation history
        chat_container = st.container()
        
        with chat_container:
            if not st.session_state.conversation_history:
                st.markdown("""
                <div style="text-align: center; padding: 3rem; opacity: 0.5;">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">🌌</div>
                    <div style="font-size: 1.2rem;">The neural network awaits your query...</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Display conversation history with feedback
            for i, message in enumerate(st.session_state.conversation_history):
                if message["role"] == "user":
                    display_chat_message(message["role"], message["content"])
                else:
                    # For assistant messages, pass the message index for feedback
                    message_index = i // 2  # Each pair (user, assistant) gets same index
                    display_chat_message(message["role"], message["content"], message_index)
        
        # Chat input
        with st.form("chat_form", clear_on_submit=True):
            user_input = st.text_area(
                "◦ Transmit your thoughts ◦",
                placeholder="Enter your query into the neural network...",
                height=100,
                key="user_input"
            )
            
            col_send, col_example = st.columns([1, 2])
            
            with col_send:
                send_button = st.form_submit_button("⚡ Transmit", use_container_width=True)
            
            with col_example:
                if st.form_submit_button("� Example Query", use_container_width=True):
                    user_input = "What mysteries of the universe can you reveal?"
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
        st.markdown('<h3 style="text-align: center; margin-bottom: 1rem; opacity: 0.8;">🔥 Neural Pathways</h3>', unsafe_allow_html=True)
        
        # Predefined prompts
        quick_prompts = [
            "🌌 Explore the cosmos",
            "⚡ Code mysteries",
            "🔮 Debug enigmas", 
            "🍃 Natural solutions",
            "🧠 Neural networks",
            "📝 Creative writing",
            "🔢 Mathematical puzzles"
        ]
        
        for prompt in quick_prompts:
            if st.button(prompt, use_container_width=True):
                # Add this prompt to conversation
                st.session_state.conversation_history.append({
                    "role": "user", 
                    "content": prompt.split(" ", 1)[1]  # Remove emoji
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
        
        st.markdown('<div style="height: 1rem;"></div>', unsafe_allow_html=True)
        
        # Learning Actions
        st.markdown('<h4 style="text-align: center; margin-bottom: 1rem; opacity: 0.8;">🧠 Learning Actions</h4>', unsafe_allow_html=True)
        
        learning_actions = [
            ("📊 View Stats", "show_stats"),
            ("🎯 Improvement", "show_improvement"),
            ("🔄 Reset Learning", "reset_learning"),
            ("💡 Get Suggestions", "get_suggestions")
        ]
        
        for action_name, action_key in learning_actions:
            if st.button(action_name, use_container_width=True, key=action_key):
                handle_learning_action(action_key)
        
        st.markdown('<div style="height: 2rem;"></div>', unsafe_allow_html=True)
        
        # Neural network info
        st.markdown(f"""
        <div class="metric-container" style="text-align: center;">
            <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">🧠</div>
            <div style="font-size: 0.9rem; opacity: 0.7;">Neural Activity</div>
            <div style="font-size: 1.2rem; font-weight: bold; margin-top: 0.5rem;">{len(st.session_state.conversation_history)} synapses</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Mysterious footer
        st.markdown("""
        <div style="text-align: center; margin-top: 2rem; opacity: 0.5; font-size: 0.8rem;">
            <div style="margin-bottom: 0.5rem;">◦ ◦ ◦</div>
            <div>Neural pathways established</div>
            <div>Quantum consciousness active</div>
            <div>✨ Nexus Protocol v2.0 ✨</div>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
