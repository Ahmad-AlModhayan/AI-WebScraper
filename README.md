# AI Web Scraper

AI Web Scraper is a dynamic and intelligent web scraping tool built using Streamlit, Selenium, and Llama 3.2. This tool allows you to scrape dynamic web pages, analyze the extracted content using AI, and perform a variety of tasks like summarization, table extraction, and more.

## Features
- **Dynamic Web Scraping**: Handles dynamic websites using Selenium with scrolling and content loading.
- **Content Cleaning**: Extracts and cleans relevant HTML content with BeautifulSoup.
- **AI-Powered Parsing**: Analyze scraped content with Llama 3.2 for various text processing tasks.
- **Streamlit Interface**: User-friendly interface for scraping and content analysis.
- **Dynamic Selector Support**: Customize scraping by specifying CSS selectors for specific elements.

## Requirements
- Docker (optional for containerized deployment)
- Python 3.10 or later

## Installation
### Step 1: Clone the Repository
```bash
git clone https://github.com/<your_username>/ai-web-scraper.git
cd ai-web-scraper
```

### Step 2: Install Dependencies
Using pip:
```bash
pip install -r requirements.txt
```

### Step 3: Run the Application
```bash
streamlit run app.py
```

The app will be available at `http://localhost:8501`.

## Containerized Deployment
### Build the Docker Image
```bash
docker build -t ai-web-scraper .
```

### Run the Container
```bash
docker run -p 8501:8501 ai-web-scraper
```

Access the app in your browser at `http://localhost:8501`.

## Usage
1. **Enter the URL**: Provide the URL of the website to scrape.
2. **Customize Selectors**: Optionally, specify CSS selectors for dynamic content.
3. **Scrape and Analyze**:
   - Scrape the website's content.
   - Use AI-powered parsing to extract or process specific content.

## Example Prompts for Parsing
- **Extract a Table**: Extract all tables from the HTML content and return them in markdown format.
- **Extract a List**: Extract all bullet-point lists from the HTML content and return them as plain text.
- **Summarize**: Summarize the main text content in 100 words.
- **Find Links**: Extract all hyperlinks (anchor tags) from the HTML and return them as a list.

## Technologies Used
- **Streamlit**: Interactive UI for web scraping and analysis.
- **Selenium**: Dynamic content scraping.
- **BeautifulSoup**: Content extraction and cleaning.
- **Llama 3.2**: AI-powered content analysis.
- **Docker**: Containerized deployment.

## Future Improvements
- Add support for CAPTCHA bypassing.
- Enhance error handling and dynamic content scraping for highly complex websites.

## Contributing
Contributions are welcome! Feel free to submit a pull request or open an issue for suggestions or bug reports.

## License
This project is licensed under the MIT License.
