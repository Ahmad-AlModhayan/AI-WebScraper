import streamlit as st
from scraper import get_page_content, clean_html, split_dom_content
from parser import ai_parse_content

# Set page configuration
st.set_page_config(
    page_title="AI Web Scraper",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load external CSS for styling
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("styles.css")

# App title
st.markdown('<div class="title">AI Web Scraper</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Scrape and analyze web content effortlessly with AI.</div>',
    unsafe_allow_html=True,
)

# Sidebar for settings
st.sidebar.header("Settings")
browser = st.sidebar.selectbox("Choose a browser:", ["Chrome", "Edge"])
parse_description = st.sidebar.text_area(
    "Parsing Instructions", "Extract all text content from the provided HTML."
)

# Input for URL
url = st.text_input("Enter the URL to scrape:")

# Session state management for scraped content
if "scraped_content" not in st.session_state:
    st.session_state["scraped_content"] = ""

# Scrape button
if st.button("Scrape"):
    if not url:
        st.warning("Please enter a valid URL to scrape.")
    else:
        with st.spinner("Scraping the web page..."):
            try:
                # Scrape and clean the content
                raw_html = get_page_content(url, browser)
                cleaned_html = clean_html(raw_html)
                st.session_state["scraped_content"] = cleaned_html
                st.success("Scraping completed successfully!")
                # Display cleaned HTML in an expandable section
                with st.expander("View Cleaned HTML Content"):
                    st.text_area("Cleaned HTML Content", cleaned_html[:1000] + "...", height=200)
            except Exception as e:
                st.error(f"Error during scraping: {e}")

# Analyze button
if st.button("Analyze"):
    if not st.session_state["scraped_content"]:
        st.warning("You need to scrape a page before analyzing.")
    else:
        with st.spinner("Analyzing the content..."):
            try:
                # Chunk the HTML content
                chunks = split_dom_content(st.session_state["scraped_content"])
                results = []
                for chunk in chunks:
                    result = ai_parse_content(chunk, parse_description)
                    results.append(result)
                # Combine results and display
                parsed_result = "\n".join(results)
                st.success("Analysis completed successfully!")
                with st.expander("View Parsed Content"):
                    st.text_area("Parsed Content", parsed_result, height=300)
            except Exception as e:
                st.error(f"Error during analysis: {e}")

# Footer
st.markdown(
    '<div class="footer">Powered by AI | Streamlit | Selenium</div>',
    unsafe_allow_html=True,
)
