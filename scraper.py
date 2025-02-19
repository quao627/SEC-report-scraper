from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from html.parser import HTMLParser
from typing import List
import time
import os

class WebScraper:
    def __init__(self, headless: bool = False):
        self.options = Options()
        if headless:
            self.options.add_argument("--headless")
        self.options.add_argument("--disable-gpu")
        self.options.add_argument("--window-size=1920x1080")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_argument("start-maximized")
        self.service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
    
    def fetch_html(self, url: str, output_file: str) -> None:
        print(f"Fetching: {url}")
        self.driver.get(url)
        time.sleep(3)  # Adjust as needed
        page_html = self.driver.page_source
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(page_html)
        print(f"Saved HTML to {output_file}")
    
    def close(self) -> None:
        self.driver.quit()

class HTMLToTextParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text: List[str] = []

    def handle_data(self, data: str) -> None:
        stripped_data = data.strip()
        if stripped_data:
            self.text.append(stripped_data)

    def get_text(self) -> str:
        return "\n".join(self.text)

class HTMLProcessor:
    @staticmethod
    def html_to_text(input_file: str, output_file: str) -> None:
        with open(input_file, "r", encoding="utf-8") as file:
            html_content = file.read()
        parser = HTMLToTextParser()
        parser.feed(html_content)
        text_content = parser.get_text()
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(text_content)
        print(f"Converted HTML to text: {output_file}")

class SECReportProcessor:
    def __init__(self, urls: List[str], output_dir: str = "sec_reports", headless: bool = False):
        self.urls = urls
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.scraper = WebScraper(headless=headless)
    
    def process_reports(self) -> None:
        for idx, url in enumerate(self.urls, start=1):
            file_name = url.split("/")[-1].split(".")[0]
            html_file = os.path.join(self.output_dir, f"{file_name}.html")
            text_file = os.path.join(self.output_dir, f"{file_name}.txt")
            self.scraper.fetch_html(url, html_file)
            HTMLProcessor.html_to_text(html_file, text_file)
        self.scraper.close()
        print("Processing complete.")

if __name__ == "__main__":
    urls = [
        "https://www.sec.gov/Archives/edgar/data/320193/000032019324000123/aapl-20240928.htm",
        "https://www.sec.gov/Archives/edgar/data/1326801/000132680125000017/meta-20241231.htm"
    ]
    processor = SECReportProcessor(urls, headless=False)
    processor.process_reports()
