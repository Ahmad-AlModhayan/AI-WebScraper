import streamlit as st
from src.core.scraper import WebScraper
from src.core.analyzer import DataAnalyzer
from src.ui.styles import apply_custom_theme, sidebar_menu
from src.utils.config import config
from src.utils.logging import logger

def main():
    """
    Main Streamlit application entry point
    Manages application routing and core components
    """
    # Apply custom UI theme
    apply_custom_theme()
    
    # Select menu option
    selected_menu = sidebar_menu()
    
    # Initialize core components
    try:
        scraper = WebScraper(headless=config.get('scraper.headless_mode', True))
        analyzer = DataAnalyzer(
            model=config.get('analyzer.model', 'llama3.2'),
            embedding_model=config.get('analyzer.embedding_model', 'sentence-transformers/all-mpnet-base-v2')
        )
    except Exception as e:
        logger.error(f"Component initialization failed: {e}")
        st.error("Failed to initialize core components. Please check your configuration.")
        return
    
    # Routing based on selected menu
    if selected_menu == "home":
        render_home_page()
    elif selected_menu == "scraper":
        render_scraper_page(scraper, analyzer)
    elif selected_menu == "analysis":
        render_analysis_page(analyzer)
    elif selected_menu == "settings":
        render_settings_page()

def render_home_page():
    """Render the landing page"""
    st.title("Welcome to AI Web Scraper Pro")
    st.markdown("""
    ### 🌐 Intelligent Web Content Extraction & Analysis
    
    Leverage cutting-edge AI to:
    - 🔍 Scrape complex web pages
    - 📊 Analyze extracted content
    - 🤖 Generate insights using Llama 3.2
    """)

def render_scraper_page(scraper, analyzer):
    """Web scraping interface"""
    st.header("🌐 Web Scraper")
    
    # URL and scraping options
    url = st.text_input("Enter Website URL", placeholder="https://example.com")
    
    # Advanced scraping options
    with st.expander("Advanced Scraping Options"):
        max_pages = st.number_input("Max Pages to Scrape", min_value=1, max_value=50, value=5)
        use_proxy = st.checkbox("Use Proxy")
    
    if st.button("Start Scraping"):
        try:
            # Perform scraping
            results = scraper.scrape(url, max_pages=max_pages, use_proxy=use_proxy)
            
            # Display results
            st.dataframe(results)
            
            # Option to analyze
            if st.button("Analyze Scraped Data"):
                analysis = analyzer.analyze_dataset(results)
                st.json(analysis)
        except Exception as e:
            st.error(f"Scraping failed: {e}")

def render_analysis_page(analyzer):
    """Data analysis interface"""
    st.header("📊 AI-Powered Data Analysis")
    
    # Upload data
    uploaded_file = st.file_uploader("Upload CSV/Excel", type=['csv', 'xlsx'])
    
    if uploaded_file:
        # Read file
        import pandas as pd
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
        
        # Analysis type selection
        analysis_type = st.selectbox(
            "Select Analysis Type", 
            ["Technical", "Summary", "Custom"]
        )
        
        if analysis_type == "Custom":
            custom_prompt = st.text_area("Enter Custom Analysis Prompt")
        else:
            custom_prompt = None
        
        if st.button("Analyze"):
            try:
                results = analyzer.analyze_dataset(
                    df, 
                    analysis_type=analysis_type, 
                    custom_prompt=custom_prompt
                )
                st.json(results)
            except Exception as e:
                st.error(f"Analysis failed: {e}")

def render_settings_page():
    """Application settings interface"""
    st.header("⚙️ Application Settings")
    
    # Display current configuration
    st.subheader("Current Configuration")
    st.json({
        "App Version": config.get('app.version'),
        "Environment": config.get('app.environment'),
        "Scraper Timeout": config.get('scraper.default_timeout'),
        "Analyzer Model": config.get('analyzer.model')
    })

if __name__ == "__main__":
    main()
