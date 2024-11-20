from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import os


def initialize_driver(browser="chrome", headless=True):
    """
    Initializes a Selenium WebDriver for the specified browser.

    Args:
        browser (str): Browser to use ("chrome" or "edge").
        headless (bool): Whether to run in headless mode.

    Returns:
        WebDriver: A Selenium WebDriver instance.
    """
    driver_path = (
        os.getenv("CHROME_DRIVER_PATH", "chromedriver.exe")
        if browser.lower() == "chrome"
        else os.getenv("EDGE_DRIVER_PATH", "msedgedriver.exe")
    )
    if not os.path.exists(driver_path):
        raise ValueError(f"Driver path not found: {driver_path}")

    options = ChromeOptions() if browser.lower() == "chrome" else EdgeOptions()
    if headless:
        options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = ChromeService(driver_path) if browser.lower() == "chrome" else EdgeService(driver_path)
    return webdriver.Chrome(service=service, options=options) if browser == "chrome" else webdriver.Edge(service=service, options=options)


def get_page_content(url: str, browser="chrome") -> str:
    """
    Fetches the HTML content of a web page using Selenium.

    Args:
        url (str): The URL of the web page to scrape.
        browser (str): Browser to use ("chrome" or "edge").

    Returns:
        str: The HTML content of the page.
    """
    try:
        driver = initialize_driver(browser=browser)
        driver.get(url)

        # Wait for the page to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        page_content = driver.page_source
        driver.quit()
        return page_content

    except Exception as e:
        if 'driver' in locals():
            driver.quit()
        raise RuntimeError(f"Error while scraping: {str(e)}")


def clean_html(raw_html: str) -> str:
    """
    Cleans raw HTML by removing unnecessary elements like scripts and styles.

    Args:
        raw_html (str): The raw HTML content.

    Returns:
        str: Cleaned HTML content.
    """
    soup = BeautifulSoup(raw_html, "html.parser")
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()
    return soup.get_text(separator="\n").strip()


def split_dom_content(content: str, max_length=3000) -> list:
    """
    Splits the DOM content into smaller chunks for AI processing.

    Args:
        content (str): The cleaned HTML content.
        max_length (int): Maximum length of each chunk.

    Returns:
        list: List of content chunks.
    """
    words = content.split()
    chunks = []
    current_chunk = []
    current_length = 0
    for word in words:
        if current_length + len(word) > max_length:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_length = 0
        current_chunk.append(word)
        current_length += len(word) + 1
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    return chunks
