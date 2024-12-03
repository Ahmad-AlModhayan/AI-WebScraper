import streamlit as st
import os
import sys

# Ensure the src directory is in the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.config import config
from src.ui.styles import (
    apply_custom_theme, 
    sidebar_menu, 
    get_current_language, 
    set_language
)
from src.core.scraper import WebScraper
from src.core.analyzer import AIAnalyzer

def main():
    # Apply custom theme based on current language
    apply_custom_theme()

    # Get current language
    current_lang = get_current_language()

    # Sidebar navigation
    selected_page = sidebar_menu()

    # Multilingual page routing
    if selected_page == "home" or selected_page == "🏠 الرئيسية":
        render_home_page()
    elif selected_page == "scraper" or selected_page == "🔍 تحليل المواقع":
        render_scraper_page()
    elif selected_page == "analysis" or selected_page == "📊 تحليل البيانات":
        render_analysis_page()
    elif selected_page == "settings" or selected_page == "⚙️ الإعدادات":
        render_settings_page()

def render_home_page():
    """Render the home page with multilingual support"""
    current_lang = get_current_language()
    
    # Multilingual page content
    page_texts = {
        'ar': {
            'title': 'مرحبًا بك في محلل المواقع',
            'description': 'أداة متقدمة لتحليل محتوى الويب باستخدام الذكاء الاصطناعي',
            'features': [
                'استخراج محتوى ذكي',
                'تحليل متعمق باستخدام AI',
                'دعم متعدد اللغات'
            ]
        },
        'en': {
            'title': 'Welcome to AI Web Scraper',
            'description': 'Advanced web content analysis tool powered by AI',
            'features': [
                'Intelligent content extraction',
                'In-depth AI analysis',
                'Multilingual support'
            ]
        }
    }
    
    texts = page_texts.get(current_lang, page_texts['en'])
    
    st.title(texts['title'])
    st.write(texts['description'])
    
    st.subheader(config.get_language_text('ui', 'features', current_lang))
    for feature in texts['features']:
        st.markdown(f"- {feature}")

def render_scraper_page():
    """Render the web scraping page with multilingual support"""
    current_lang = get_current_language()
    
    # Multilingual page content
    url_placeholder = config.get_language_text('ui', 'enter_url', current_lang)
    scrape_button = config.get_language_text('ui', 'start_scraping', current_lang)
    
    # URL input
    url = st.text_input(url_placeholder)
    
    # Scraping options
    max_pages = st.number_input(
        config.get_language_text('ui', 'max_pages', current_lang), 
        min_value=1, 
        max_value=50, 
        value=10
    )
    
    use_proxy = st.checkbox(config.get_language_text('ui', 'use_proxy', current_lang))
    
    if st.button(scrape_button):
        if url:
            try:
                scraper = WebScraper()
                results = scraper.scrape(
                    url, 
                    max_pages=max_pages, 
                    use_proxy=use_proxy
                )
                st.success(config.get_language_text('ui', 'success', current_lang))
                st.json(results)
            except Exception as e:
                st.error(f"{config.get_language_text('ui', 'error', current_lang)}: {str(e)}")
        else:
            st.warning(config.get_language_text('ui', 'enter_url', current_lang))

def render_analysis_page():
    """Render the data analysis page with multilingual support"""
    current_lang = get_current_language()
    
    # Multilingual page content
    st.subheader(config.get_language_text('ui', 'analysis', current_lang))
    
    # Analysis type selection
    analysis_types = {
        'ar': {
            'summary': 'ملخص',
            'technical': 'تحليل تقني',
            'custom': 'تحليل مخصص'
        },
        'en': {
            'summary': 'Summary',
            'technical': 'Technical',
            'custom': 'Custom'
        }
    }
    
    # File uploader
    uploaded_file = st.file_uploader(
        config.get_language_text('ui', 'upload_file', current_lang)
    )
    
    # Analysis type selection
    analysis_type = st.selectbox(
        config.get_language_text('ui', 'select_analysis', current_lang),
        list(analysis_types[current_lang].values())
    )
    
    # Custom prompt for custom analysis
    if analysis_type == analysis_types[current_lang]['custom']:
        custom_prompt = st.text_area(
            config.get_language_text('ui', 'custom_prompt', current_lang)
        )
    
    # Analyze button
    if st.button(config.get_language_text('ui', 'analyze', current_lang)):
        if uploaded_file:
            try:
                analyzer = AIAnalyzer()
                
                # Determine analysis type
                if analysis_type == analysis_types[current_lang]['summary']:
                    results = analyzer.summarize(uploaded_file)
                elif analysis_type == analysis_types[current_lang]['technical']:
                    results = analyzer.technical_analysis(uploaded_file)
                else:
                    results = analyzer.custom_analysis(
                        uploaded_file, 
                        custom_prompt if 'custom_prompt' in locals() else None
                    )
                
                st.success(config.get_language_text('ui', 'success', current_lang))
                st.json(results)
            except Exception as e:
                st.error(f"{config.get_language_text('ui', 'error', current_lang)}: {str(e)}")
        else:
            st.warning(config.get_language_text('ui', 'upload_file', current_lang))

def render_settings_page():
    """Render the settings page with multilingual support"""
    current_lang = get_current_language()
    
    st.header(config.get_language_text('ui', 'settings', current_lang))
    
    # Language selection
    st.subheader(config.get_language_text('ui', 'select_language', current_lang))
    
    languages = {
        'ar': 'العربية',
        'en': 'English'
    }
    
    selected_lang = st.selectbox(
        config.get_language_text('ui', 'select_language', current_lang),
        list(languages.keys()),
        format_func=lambda x: languages[x],
        index=list(languages.keys()).index(current_lang)
    )
    
    if selected_lang != current_lang:
        set_language(selected_lang)
        st.experimental_rerun()

if __name__ == "__main__":
    main()
