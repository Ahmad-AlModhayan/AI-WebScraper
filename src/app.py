import streamlit as st
import os
import sys
import pandas as pd

# Ensure the src directory is in the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.config import config
from src.ui.styles import (
    apply_custom_theme, 
    sidebar_menu, 
    get_current_language, 
    set_language,
    loading_spinner,
    success_message,
    error_message
)
from src.core.scraper import WebScraper
from src.core.analyzer import AIAnalyzer

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
            'title': 'Welcome to Web Scraper Pro',
            'description': 'Advanced web content analysis tool powered by AI',
            'features': [
                'Intelligent content extraction',
                'Deep AI-powered analysis',
                'Multilingual support'
            ]
        }
    }
    
    st.title(page_texts[current_lang]['title'])
    st.write(page_texts[current_lang]['description'])
    
    # Feature list
    st.subheader(
        "الميزات الرئيسية" if current_lang == 'ar' else "Key Features"
    )
    for feature in page_texts[current_lang]['features']:
        st.markdown(f"- {feature}")

def render_scraper_page():
    """Render the web scraping page with multilingual support"""
    current_lang = get_current_language()
    
    # Multilingual text
    texts = {
        'ar': {
            'title': 'أداة استخراج محتوى الويب',
            'url_label': 'أدخل رابط الموقع للاستخراج',
            'scrape_button': 'استخراج المحتوى',
            'max_pages_label': 'الحد الأقصى لعدد الصفحات'
        },
        'en': {
            'title': 'Web Content Extraction Tool',
            'url_label': 'Enter website URL to scrape',
            'scrape_button': 'Scrape Content',
            'max_pages_label': 'Maximum number of pages'
        }
    }
    
    st.title(texts[current_lang]['title'])
    
    # URL input
    url = st.text_input(texts[current_lang]['url_label'], 
                        placeholder="https://example.com")
    
    # Max pages input
    max_pages = st.number_input(
        texts[current_lang]['max_pages_label'], 
        min_value=1, 
        max_value=50, 
        value=5
    )
    
    # Scrape button
    if st.button(texts[current_lang]['scrape_button']):
        if not url:
            error_message("الرجاء إدخال رابط صالح" if current_lang == 'ar' else "Please enter a valid URL")
            return
        
        with loading_spinner(current_lang):
            try:
                # Initialize scraper with proper configuration
                scraper = WebScraper(
                    timeout=30,  # 30 second timeout
                    language=current_lang
                )
                
                # Perform scraping with proper error handling
                try:
                    results = scraper.scrape(url, max_pages=max_pages)
                    
                    if not results:
                        error_message(
                            "لم يتم العثور على محتوى في هذا الموقع" 
                            if current_lang == 'ar' 
                            else "No content found on this website"
                        )
                        return
                        
                    # Display results
                    st.subheader(
                        "نتائج الاستخراج" if current_lang == 'ar' else "Scraping Results"
                    )
                    
                    for result in results:
                        st.markdown(f"**URL:** {result['url']}")
                        st.markdown(f"**Page:** {result['page']}")
                        
                        if 'tools' in result and result['tools']:
                            for tool in result['tools']:
                                with st.expander(f"🛠️ {tool.get('name', 'Unknown Tool')}"):
                                    st.markdown(f"**Description:** {tool.get('description', 'No description')}")
                                    st.markdown(f"**Category:** {tool.get('category', 'Uncategorized')}")
                                    st.markdown(f"**Rating:** {tool.get('rating', 'N/A')}")
                        else:
                            st.warning(
                                "تم الوصول للصفحة ولكن لم يتم العثور على أدوات" 
                                if current_lang == 'ar' 
                                else "Page accessed but no tools found"
                            )
                    
                    success_message(
                        "تم استخراج المحتوى بنجاح" 
                        if current_lang == 'ar' 
                        else "Content scraped successfully"
                    )
                
                except Exception as e:
                    error_message(
                        f"خطأ في الاستخراج: {str(e)}" 
                        if current_lang == 'ar' 
                        else f"Scraping error: {str(e)}"
                    )
            
            except Exception as e:
                error_message(
                    f"خطأ في الاستخراج: {str(e)}" 
                    if current_lang == 'ar' 
                    else f"Scraping error: {str(e)}"
                )

def render_analysis_page():
    """Render the data analysis page with multilingual support"""
    current_lang = get_current_language()
    
    # Multilingual text
    texts = {
        'ar': {
            'title': 'تحليل البيانات باستخدام الذكاء الاصطناعي',
            'upload_label': 'تحميل ملف البيانات',
            'analyze_button': 'تحليل البيانات',
            'analysis_type_label': 'اختر نوع التحليل'
        },
        'en': {
            'title': 'AI-Powered Data Analysis',
            'upload_label': 'Upload Data File',
            'analyze_button': 'Analyze Data',
            'analysis_type_label': 'Select Analysis Type'
        }
    }
    
    st.title(texts[current_lang]['title'])
    
    # File upload
    uploaded_file = st.file_uploader(
        texts[current_lang]['upload_label'], 
        type=['csv', 'json', 'xlsx', 'txt']
    )
    
    # Analysis type selection
    analysis_types = {
        'ar': {
            'تلخيص': 'summarize',
            'تحليل تقني': 'technical_analysis',
            'تحليل مخصص': 'custom_analysis'
        },
        'en': {
            'Summarization': 'summarize',
            'Technical Analysis': 'technical_analysis',
            'Custom Analysis': 'custom_analysis'
        }
    }
    
    analysis_type = st.selectbox(
        texts[current_lang]['analysis_type_label'], 
        list(analysis_types[current_lang].keys())
    )
    
    # Analyze button
    if st.button(texts[current_lang]['analyze_button']) and uploaded_file:
        with loading_spinner(current_lang):
            try:
                # Read uploaded file
                if uploaded_file.type == 'application/json':
                    df = pd.read_json(uploaded_file)
                elif uploaded_file.type == 'text/csv':
                    df = pd.read_csv(uploaded_file)
                elif uploaded_file.type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
                    df = pd.read_excel(uploaded_file)
                else:
                    df = pd.read_csv(uploaded_file, sep='\t')
                
                # Initialize AI Analyzer
                analyzer = AIAnalyzer(language=current_lang)
                
                # Perform analysis based on selected type
                analysis_method = getattr(analyzer, 
                    analysis_types[current_lang][analysis_type]
                )
                
                # Analyze data
                results = analysis_method(df)
                
                # Display results
                st.subheader(
                    "نتائج التحليل" if current_lang == 'ar' else "Analysis Results"
                )
                st.write(results)
                
                success_message(
                    "تم إجراء التحليل بنجاح" 
                    if current_lang == 'ar' 
                    else "Analysis completed successfully"
                )
            
            except Exception as e:
                error_message(
                    f"خطأ في التحليل: {str(e)}" 
                    if current_lang == 'ar' 
                    else f"Analysis error: {str(e)}"
                )

def render_settings_page():
    """Render the settings page with multilingual support"""
    current_lang = get_current_language()
    
    # Multilingual text
    texts = {
        'ar': {
            'title': 'الإعدادات',
            'language_label': 'اختر اللغة',
            'save_button': 'حفظ الإعدادات'
        },
        'en': {
            'title': 'Settings',
            'language_label': 'Select Language',
            'save_button': 'Save Settings'
        }
    }
    
    st.title(texts[current_lang]['title'])
    
    # Language selection
    language_options = {
        'ar': 'العربية',
        'en': 'English'
    }
    
    selected_language = st.selectbox(
        texts[current_lang]['language_label'], 
        list(language_options.values())
    )
    
    # Map display value to language code
    language_map = {v: k for k, v in language_options.items()}
    
    # Save button
    if st.button(texts[current_lang]['save_button']):
        # Set language
        new_lang = language_map[selected_language]
        set_language(new_lang)
        
        success_message(
            f"تم تغيير اللغة إلى {language_options[new_lang]}" 
            if current_lang == 'ar' 
            else f"Language changed to {language_options[new_lang]}"
        )

def main():
    # Apply custom theme based on current language
    apply_custom_theme()

    # Get current language
    current_lang = get_current_language()

    # Sidebar navigation
    selected_page = sidebar_menu()

    # Multilingual page routing
    if selected_page == "🏠 الرئيسية" or selected_page == "🏠 Home":
        render_home_page()
    elif selected_page == "🔍 تحليل المواقع" or selected_page == "🔍 Web Scraper":
        render_scraper_page()
    elif selected_page == "📊 تحليل البيانات" or selected_page == "📊 Data Analysis":
        render_analysis_page()
    elif selected_page == "⚙️ الإعدادات" or selected_page == "⚙️ Settings":
        render_settings_page()

if __name__ == "__main__":
    main()
