import selenium
import time
from selenium.webdriver import Edge
from selenium.webdriver.edge.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.edge.service import Service
service2 = Service("msedgedriver.exe")

options2 = webdriver.EdgeOptions()
driver2 = webdriver.Edge(service=service2, options=options2)
# Initialize the WebDriver

try:
    # Navigate to Wikipedia
    driver2.get('https://www.wikipedia.org/')
    time.sleep(2)  # Allow some time for the page to load

    # Find the Wikipedia logo by its class or other attributes
    logo = driver2.find_element(By.CLASS_NAME, 'central-featured-logo')

    # Get the dimensions of the logo
    logo_size = logo.size

    # Check if the width and height are both 160px
    if logo_size['width'] == 160 and logo_size['height'] == 160:
        print("The Wikipedia logo dimensions are correct: 160x160px")
    else:
        print("The Wikipedia logo dimensions are incorrect.")
        print(f"Actual dimensions: {logo_size['width']}x{logo_size['height']}px")

finally:
    # Close the browser
    driver2.quit()
