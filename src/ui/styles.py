import streamlit as st

def apply_custom_theme():
    """Apply a modern, clean UI theme"""
    st.set_page_config(
        page_title="AI Web Scraper Pro",
        page_icon="🌐",
        layout="wide"
    )
    
    # Custom CSS for enhanced UI
    st.markdown("""
    <style>
    /* Global Styles */
    body {
        color: #333;
        background-color: #f4f6f9;
        font-family: 'Inter', sans-serif;
    }
    
    /* Streamlit Specific Overrides */
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #3498db;
        color: white;
        border-radius: 5px;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #2980b9;
        transform: scale(1.05);
    }
    
    /* Sidebar */
    .css-1aumxhk {
        background-color: #ffffff;
        border-right: 1px solid #e0e0e0;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #2c3e50;
        font-weight: 600;
    }
    
    /* Data Display */
    .stDataFrame {
        border: 1px solid #e0e0e0;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

def sidebar_menu():
    """Create a dynamic sidebar menu"""
    st.sidebar.title("🌐 AI Web Scraper Pro")
    
    menu_options = {
        "🏠 Home": "home",
        "🔍 Web Scraper": "scraper",
        "📊 Data Analysis": "analysis",
        "⚙️ Settings": "settings"
    }
    
    selected_option = st.sidebar.radio("Navigation", list(menu_options.keys()))
    
    return menu_options[selected_option]

def loading_spinner():
    """Custom loading spinner with context"""
    return st.spinner("🔍 Analyzing content... This might take a moment.")

def success_message(message):
    """Enhanced success notification"""
    st.success(f"✅ {message}")

def error_message(message):
    """Enhanced error notification"""
    st.error(f"❌ {message}")

def info_message(message):
    """Enhanced info notification"""
    st.info(f"ℹ️ {message}")
