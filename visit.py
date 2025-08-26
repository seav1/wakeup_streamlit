from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import sys

URL = "https://seav01.streamlit.app/"

def setup_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--remote-debugging-port=9222')
    options.binary_location = '/usr/bin/chromium-browser'
    
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        return driver
    except Exception as e:
        print(f"Failed to setup driver: {e}")
        sys.exit(1)

def main():
    driver = setup_driver()
    
    try:
        print(f"Navigating to {URL}")
        driver.get(URL)
        print("Page opened, waiting for content to load...")
        
        # Wait for page to load completely
        WebDriverWait(driver, 30).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        
        # Look for the wake-up button with explicit wait
        try:
            button = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Yes, get this app back up!')]"))
            )
            button.click()
            print("Successfully clicked wake-up button.")
        except Exception as e:
            print(f"No wake-up button found or app already awake: {e}")
        
        # Wait for app to respond
        time.sleep(15)
        print("Visit completed successfully.")
        
    except Exception as e:
        print(f"Error during execution: {e}")
        sys.exit(1)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
