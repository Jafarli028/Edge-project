import selenium
import time
from selenium.webdriver import Edge
from selenium.webdriver.edge.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.edge.service import Service

# Set the path to the Microsoft Edge driver executable
edge_driver_path = 'msedgedriver.exe'

# Create a service object for the Edge driver
service = Service(executable_path=edge_driver_path)

# Create an instance of the Edge driver
driver = webdriver.Edge(service=service)

try:
    # Open Wikipedia's main page
    driver.get('https://en.wikipedia.org/wiki/NASA')

    # Wait for the page to load
    driver.implicitly_wait(10)  # Wait up to 10 seconds for elements to appear

    # Get the computed style of the body element
    body_element = driver.find_element(By.TAG_NAME, 'body')
    body_style = driver.execute_script("return window.getComputedStyle(arguments[0]).backgroundColor", body_element)

    # Print the background color
    print(f"The background color of the Wikipedia page is: {body_style}")

finally:
    # Close the browser
    driver.quit()