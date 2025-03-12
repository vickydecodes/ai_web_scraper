from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def scrape_website(website):
    print("Launching browser...")
    
    options = Options()
    options.add_argument("--headless=new")  # Use the updated headless mode
    options.add_argument("--disable-popup-blocking")  # Block pop-ups
    options.add_argument("--disable-notifications")  # Disable site notifications
    options.add_argument("--ignore-certificate-errors")  # Ignore SSL errors
    options.add_argument("--log-level=3")  # Reduce logs in the terminal
    options.add_argument("--window-size=1920,1080")  # Set a fixed window size for stability
    options.add_argument("--blink-settings=imagesEnabled=false")  # Disable image loading for faster scraping

    # Automatically install and use the correct ChromeDriver version
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        driver.get(website)
        print("Page loaded..")
        html = driver.page_source
        time.sleep(10)  # Consider reducing this to 3-5 seconds
        
        return html
    finally:
        driver.quit()

def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""

def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")

    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )

    return cleaned_content

def split_dom_content(dom_content, max_length=6000):
    return [
        dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)
    ]


def find_all_links(html_content, base_url):
    soup = BeautifulSoup(html_content, "html.parser")
    links = set()
    
    for a_tag in soup.find_all("a", href=True):
        href = a_tag.get("href")
        full_url = urljoin(base_url, href)
        if base_url in full_url:  # Only add internal links
            links.add(full_url)
    
    return list(links)