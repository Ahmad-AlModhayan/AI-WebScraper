# AI Web Scraper

The **AI Web Scraper** is a powerful, modular, and deployable tool designed to scrape and analyze data from dynamic websites. Using Selenium for scraping and Ollama for AI-powered parsing, this tool serves as a foundational project for collecting real-world data for future applications.

---

## Features

- **Dynamic Web Scraping**:

  - Handles JavaScript-heavy websites using Selenium.
  - Supports multiple browsers (Edge and Chrome).
  - Extracts clean, structured data from web pages.
- **AI-Powered Parsing**:

  - Integrates with Ollama for natural language understanding and analysis.
  - Extracts insights based on user-defined queries (e.g., "Summarize this content").
- **Modular Design**:

  - Separate components for scraping, parsing, and user interaction.
  - Easily extensible for additional features or new projects.
- **Deployable Anywhere**:

  - Fully containerized with Docker for consistent performance across environments.
  - User-friendly interface built with Streamlit for quick interactions.

---

## Prerequisites

Before using the project, ensure the following are installed:

- **Python**: Version 3.8 or later
- **Pip**: For managing Python packages
- **Selenium**: Included in `requirements.txt`
- **WebDriver**: Install `msedgedriver` or `chromedriver` depending on your browser
- **Docker** (optional): For containerization
- **Ollama**: For AI-based parsing

---

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/your-repo/ai-web-scraper.git
   cd ai-web-scraper
   ```
2. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```
3. **Set Up WebDriver**:

   - **Edge**: Download [EdgeDriver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/) and place it in your project directory.
   - **Chrome**: Download [ChromeDriver](https://googlechromelabs.github.io/chrome-for-testing/) and place it in your project directory.
4. **Configure Docker** (optional):

   - Build the Docker image:
     ```bash
     docker build -t ai_web_scraper .
     ```

---

## Usage

### Run the Application Locally

1. **Run the Streamlit App**:

   ```bash
   streamlit run app.py
   ```
2. **Open the App**:

   - Access the app in your browser at `http://localhost:8501`.
3. **Scrape and Parse**:

   - Enter the URL to scrape.
   - Define a query for parsing (e.g., "Extract all links" or "Summarize content").

### Run with Docker

1. **Start the Docker Container**:

   ```bash
   docker run -p 8501:8501 ai_web_scraper
   ```
2. **Access the App**:

   - Open your browser and go to `http://localhost:8501`.

---

## Project Structure

```
AI_Web_Scraper/
├── app.py                 # Main Streamlit app
├── scraper.py             # Web scraping functions
├── parser.py              # AI-powered content parsing
├── requirements.txt       # Dependencies
├── Dockerfile             # Docker setup for deployment
└── README.md              # Project documentation
```

---

## Example Use Case

1. **Scenario**: Scrape a news website to extract the latest articles.
2. **Steps**:
   - Input the news website URL in the app.
   - Provide a query like "Extract article titles and links."
   - View the parsed results in the app or download them as a CSV.

---

## Future Enhancements

- Add support for more browsers (e.g., Firefox).
- Integrate additional AI models for enhanced parsing.
- Create an API endpoint for remote scraping and analysis.

---

## Contributing

We welcome contributions! To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request for review.

---

## License

This project is licensed under the MIT License. See `LICENSE` for more details.
