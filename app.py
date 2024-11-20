import streamlit as st
from scraper.scraper import scrape_website, extract_body_content, clean_body_content, split_dom_content
from parser.parser import ai_parse_content
import validators
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Set page configuration
st.set_page_config(page_title="AI Web Scraper", page_icon="🌐", layout="wide")

# Load custom CSS
def load_css():
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# App title and subtitle
st.markdown('<div class="title">AI Web Scraper</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Scrape and analyze dynamic web content effortlessly with AI.</div>', unsafe_allow_html=True)

# Sidebar settings
st.sidebar.header("Settings")
url = st.sidebar.text_input("Enter the URL to scrape:", placeholder="https://www.airbnb.com")
dynamic_selector = st.sidebar.text_input("Dynamic Content Selector (optional):", placeholder=".listing")
max_chunk_size = st.sidebar.slider("Chunk Size (characters):", min_value=1000, max_value=10000, value=6000)
headless_mode = st.sidebar.checkbox("Run in Headless Mode", value=True)

# Session state for managing scraped content
if "scraped_content" not in st.session_state:
    st.session_state["scraped_content"] = ""

# Parsing instructions
st.markdown("### Parsing Instructions")
instructions_placeholder = st.empty()
parse_description = instructions_placeholder.text_area(
    "Describe what you want to extract:", "Extract all text content from the provided HTML.", height=150
)

# Sample prompts for parsing
st.markdown("#### Sample Prompts")
st.markdown("""
- **Make a table**: Extract all tables from the HTML content and return them in markdown format.
- **Make a list**: Extract all bullet-point lists from the HTML content and return them as plain text.
- **Summarize**: Summarize the main text content in 100 words.
- **Find Links**: Extract all hyperlinks (anchor tags) from the HTML and return them as a list.
""")

# Clear button for parsing instructions
if st.button("Clear Instructions"):
    parse_description = instructions_placeholder.text_area(
        "Describe what you want to extract:", "", height=150
    )

# Scrape button
if st.button("Scrape"):
    if not url:
        st.warning("Please enter a valid URL to scrape.")
    elif not validators.url(url):
        st.error("Please provide a valid URL.")
    else:
        with st.spinner("Scraping the web page..."):
            try:
                # Scrape the website
                raw_html = scrape_website(url, dynamic_selector=dynamic_selector, headless=headless_mode)
                if raw_html is None:
                    st.error("Failed to scrape the website. Please check the URL and try again.")
                    st.stop()

                # Extract body content
                body_content = extract_body_content(raw_html)

                # Clean the body content
                cleaned_html = clean_body_content(body_content)

                # Save cleaned content in session state
                st.session_state["scraped_content"] = cleaned_html

                # Display scraped content
                st.success("Scraping completed successfully!")
                with st.expander("View Cleaned HTML Content"):
                    st.text_area("Cleaned HTML Content", cleaned_html[:2000] + "...", height=400)
            except Exception as e:
                st.error(f"Error during scraping: {e}")

# Analyze button
if st.session_state["scraped_content"]:
    if st.button("Analyze"):
        with st.spinner("Analyzing content..."):
            try:
                # Split content into chunks
                chunks = split_dom_content(st.session_state["scraped_content"], max_chunk_size)

                # Analyze each chunk using AI
                results = []
                for i, chunk in enumerate(chunks):
                    result = ai_parse_content(chunk, parse_description)
                    results.append(result)

                # Display parsed results
                parsed_result = "\n".join(results)
                st.success("Analysis completed successfully!")
                with st.expander("View Parsed Content"):
                    st.text_area("Parsed Content", parsed_result, height=300)
            except Exception as e:
                st.error(f"Error during analysis: {e}")

# Footer
st.markdown('<div class="footer">Powered by Ahmad AlModhayan</div>', unsafe_allow_html=True)
