# app.py
import streamlit as st
from scraper import get_page_content, extract_body_content
from parser import ai_parse_content

st.title("AI Web Scraper")

url = st.text_input("Enter the URL to scrape:")
prompt = st.text_area("Enter a prompt for AI parsing (e.g., 'Summarize this content'):")

if st.button("Scrape and Parse"):
    if url:
        st.write("Scraping the website...")
        raw_html = get_page_content(url)
        cleaned_content = extract_body_content(raw_html)
        
        st.write("Parsing content with AI...")
        result = ai_parse_content(cleaned_content, prompt)
        
        st.write("Parsed Result:")
        st.write(result)
    else:
        st.error("Please enter a valid URL.")
