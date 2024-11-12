from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from bs4 import BeautifulSoup

def initialize_driver(browser="edge", headless=True):
    # Set up options based on browser type
    if browser.lower() == "chrome":
        driver_path = "/path/to/chromedriver"  # Replace with ChromeDriver path
        options = ChromeOptions()
        service = ChromeService(driver_path)
    elif browser.lower() == "edge":
        driver_path = "msedgedriver.exe"  # Replace with EdgeDriver path
        options = EdgeOptions()
        service = EdgeService(driver_path)
    else:
        raise ValueError("Unsupported browser. Choose 'chrome' or 'edge'.")

    # Set headless option if desired
    if headless:
        options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    return webdriver.Chrome(service=service, options=options) if browser.lower() == "chrome" else webdriver.Edge(service=service, options=options)

def get_page_content(url, browser="edge"):
    driver = initialize_driver(browser=browser)
    driver.get(url)
    page_content = driver.page_source
    driver.quit()
    return page_content

def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    return body_content.get_text(strip=True) if body_content else ""
