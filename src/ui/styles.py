import streamlit as st
from typing import Literal, Dict
import logging

logger = logging.getLogger(__name__)

def set_language_styles(language: Literal['ar', 'en'] = 'ar'):
    """
    Apply language-specific styling and direction
    
    Args:
        language (str): Language to apply ('ar' or 'en')
    """
    # Font selection based on language
    fonts = {
        'ar': "'Cairo', sans-serif",
        'en': "'Inter', sans-serif"
    }
    
    # Text direction and alignment
    direction = 'rtl' if language == 'ar' else 'ltr'
    text_align = 'right' if language == 'ar' else 'left'
    
    # Language-specific CSS
    st.markdown(f"""
    <style>
    body {{
        font-family: {fonts[language]};
        direction: {direction};
        text-align: {text_align};
    }}
    
    /* Ensure proper text alignment for different components */
    .stMarkdown, .stTextInput, .stButton, .stRadio {{
        text-align: {text_align};
    }}
    
    /* Adjust sidebar and radio button layout */
    .css-1aumxhk {{
        text-align: {text_align};
    }}
    
    .stRadio > div {{
        flex-direction: {'column' if language == 'ar' else 'column'};
        align-items: {'flex-end' if language == 'ar' else 'flex-start'};
    }}
    </style>
    """, unsafe_allow_html=True)

def get_current_language() -> str:
    """
    Get the current application language
    
    Returns:
        str: Current language code ('ar' or 'en')
    """
    # Default to Arabic if not set
    return st.session_state.get('language', 'ar')

def set_language(language: str):
    """
    Set the application language in session state
    
    Args:
        language (str): Language code ('ar' or 'en')
    """
    # Validate language input
    if language not in ['ar', 'en']:
        logger.warning(f"Invalid language: {language}. Defaulting to Arabic.")
        language = 'ar'
    
    # Set language in session state
    st.session_state['language'] = language
    
    # Optional: Trigger a rerun to apply language changes
    st.experimental_rerun()

def sidebar_menu():
    """
    Create a multilingual sidebar menu with language-specific icons and titles
    
    Returns:
        str: Selected menu item
    """
    # Get current language
    current_lang = get_current_language()
    
    # Multilingual menu configuration
    menu_config = {
        'ar': {
            'home': '🏠 الرئيسية',
            'scraper': '🔍 تحليل المواقع',
            'analysis': '📊 تحليل البيانات',
            'settings': '⚙️ الإعدادات'
        },
        'en': {
            'home': '🏠 Home',
            'scraper': '🔍 Web Scraper',
            'analysis': '📊 Data Analysis',
            'settings': '⚙️ Settings'
        }
    }
    
    # Select menu items based on current language
    menu_items = menu_config[current_lang]
    
    # Create sidebar menu
    with st.sidebar:
        # Sidebar title
        st.title(
            "أدوات تحليل الويب" if current_lang == 'ar' else "Web Analysis Tools"
        )
        
        # Menu selection
        selected_page = st.radio(
            "اختر صفحة" if current_lang == 'ar' else "Select Page", 
            list(menu_items.values())
        )
    
    # Return the selected page
    return selected_page

def loading_spinner(language: Literal['ar', 'en'] = 'ar') -> st.spinner:
    """
    Create a context manager for loading spinner with language support
    
    Args:
        language (str): Current language
    
    Returns:
        st.spinner context manager
    """
    messages = {
        'ar': ' جارٍ التحليل... قد يستغرق هذا بعض الوقت',
        'en': ' Analyzing content... This might take a moment'
    }
    return st.spinner(messages[language])

def success_message(message: str, language: Literal['ar', 'en'] = 'ar') -> None:
    """
    Display a success message
    
    Args:
        message (str): Message to display
        language (str): Current language
    """
    st.success(f" {message}")

def error_message(message: str, language: Literal['ar', 'en'] = 'ar') -> None:
    """
    Display an error message
    
    Args:
        message (str): Message to display
        language (str): Current language
    """
    st.error(f" {message}")

def info_message(message: str, language: Literal['ar', 'en'] = 'ar') -> None:
    """
    Display an informational message
    
    Args:
        message (str): Message to display
        language (str): Current language
    """
    st.info(f" {message}")

# Backward compatibility function
def apply_custom_theme():
    """
    Backward compatibility function for theme application
    """
    import warnings
    warnings.warn(
        "apply_custom_theme() is deprecated. Use set_language_styles() instead.", 
        DeprecationWarning, 
        stacklevel=2
    )
    current_language = get_current_language()
    set_language_styles(current_language)
