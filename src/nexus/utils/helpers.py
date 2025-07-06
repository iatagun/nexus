"""
Utility functions for Nexus AI Assistant
"""

import subprocess
import sys
import requests
from typing import Tuple, Optional


def check_ollama_status(host: str = "http://localhost:11434") -> Tuple[bool, Optional[str]]:
    """
    Check if Ollama is running and accessible
    
    Args:
        host: Ollama host URL
        
    Returns:
        Tuple of (is_running, error_message)
    """
    try:
        response = requests.get(f"{host}/api/tags", timeout=5)
        if response.status_code == 200:
            return True, None
        else:
            return False, f"Ollama responded with status {response.status_code}"
    except requests.exceptions.ConnectionError:
        return False, "Cannot connect to Ollama. Make sure Ollama is running."
    except requests.exceptions.Timeout:
        return False, "Timeout connecting to Ollama"
    except Exception as e:
        return False, f"Error checking Ollama status: {e}"


def start_ollama_if_needed() -> bool:
    """
    Try to start Ollama if it's not running
    
    Returns:
        True if Ollama is running after attempt, False otherwise
    """
    # First check if it's already running
    is_running, _ = check_ollama_status()
    if is_running:
        return True
    
    print("🔄 Ollama not detected. Attempting to start...")
    
    try:
        # Try to start Ollama in background
        if sys.platform == "win32":
            subprocess.Popen(["ollama", "serve"], 
                           creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:
            subprocess.Popen(["ollama", "serve"], 
                           stdout=subprocess.DEVNULL, 
                           stderr=subprocess.DEVNULL)
        
        # Wait a moment for it to start
        import time
        time.sleep(3)
        
        # Check again
        is_running, error = check_ollama_status()
        if is_running:
            print("✅ Ollama started successfully!")
            return True
        else:
            print(f"❌ Failed to start Ollama: {error}")
            return False
            
    except FileNotFoundError:
        print("❌ Ollama not found in PATH. Please install Ollama first.")
        return False
    except Exception as e:
        print(f"❌ Error starting Ollama: {e}")
        return False


def check_interactive_environment() -> bool:
    """
    Check if we're running in an interactive environment
    
    Returns:
        True if interactive, False otherwise
    """
    return sys.stdin.isatty() and sys.stdout.isatty()


def get_terminal_size() -> Tuple[int, int]:
    """
    Get terminal size for formatting
    
    Returns:
        Tuple of (width, height)
    """
    try:
        import shutil
        size = shutil.get_terminal_size()
        return size.columns, size.lines
    except:
        return 80, 24  # Default fallback
