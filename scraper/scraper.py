from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

def initialize_driver(browser="chrome", headless=True):
    """
    Initializes a local WebDriver for Chrome.

    Args:
        browser (str): Browser to use ("chrome").
        headless (bool): Whether to run in headless mode.

    Returns:
        WebDriver: Selenium WebDriver instance.
    """
    driver_path = "chromedriver.exe"  # Update with the correct path to your ChromeDriver
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = ChromeService(driver_path)
    return webdriver.Chrome(service=service, options=options)

def scrape_website(url, dynamic_selector=None, headless=True):
    """
    Scrapes the HTML content of the given URL using Selenium.

    Args:
        url (str): The URL to scrape.
        dynamic_selector (str): Selector for dynamic content to wait for (optional).
        headless (bool): Whether to run the browser in headless mode.

    Returns:
        str: HTML content of the page.
    """
    try:
        driver = initialize_driver(headless=headless)
        driver.get(url)

        # Wait for dynamic content if specified
        if dynamic_selector:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, dynamic_selector)))

        # Scroll to load all dynamic content
        scroll_down(driver)

        # Get page source
        html_content = driver.page_source
        driver.quit()
        return html_content
    except Exception as e:
        if 'driver' in locals():
            driver.quit()
        raise RuntimeError(f"Error during scraping: {e}")

def scroll_down(driver, pause_time=2):
    """
    Simulates scrolling down the webpage to load dynamic content.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        pause_time (int): Pause time between scrolls (seconds).
    """
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def extract_body_content(html_content):
    """
    Extracts the <body> content from the HTML.

    Args:
        html_content (str): Full HTML content.

    Returns:
        str: Extracted body content.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    return str(body_content) if body_content else ""

def clean_body_content(body_content):
    """
    Cleans the body content by removing unnecessary tags and extracting text.

    Args:
        body_content (str): Raw body content.

    Returns:
        str: Cleaned text content.
    """
    soup = BeautifulSoup(body_content, "html.parser")

    # Remove script and style elements
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    # Extract and clean text content
    cleaned_content = soup.get_text(separator="\n")
    return "\n".join(line.strip() for line in cleaned_content.splitlines() if line.strip())

def split_dom_content(dom_content, max_length=6000):
    """
    Splits the DOM content into smaller chunks for processing.

    Args:
        dom_content (str): Cleaned DOM content.
        max_length (int): Maximum length of each chunk.

    Returns:
        list: List of content chunks.
    """
    return [dom_content[i:i + max_length] for i in range(0, len(dom_content), max_length)]
