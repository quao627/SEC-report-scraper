# scraper for SEC reports

## Overview
This program scrapes SEC reports using a selenium driver. Simply replace the `urls` variable with the desired SEC report URLs and run `scraper.py`. The program will download the reports in the `sec_reports` directory.

**Important Notes:**
- Use `headless=False` to reduce detection as a bot.
- Not tested on a remote server.

## Installation
Follow the official guide: [Selenium WebDriver Installation](https://www.selenium.dev/documentation/webdriver/getting_started/install_library/)