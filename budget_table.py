from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set the path to the Microsoft Edge driver executable
edge_driver_path = 'msedgedriver.exe'

# Create a service object for the Edge driver
service = Service(executable_path=edge_driver_path)

# Create an instance of the Edge driver
driver = webdriver.Edge(service=service)

try:
    # Open the Wikipedia page with the budget table
    driver.get('https://en.wikipedia.org/wiki/NASA')

    # Wait for the budget table to load and be visible
    wait = WebDriverWait(driver, 10)
    # Assuming the first table with the class 'wikitable' is the budget table
    budget_table = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'table.wikitable')))

    # Get the first cell in the table
    first_cell = budget_table.find_element(By.TAG_NAME, 'td')

    # Get the computed style of the first cell
    box_sizing_style = driver.execute_script("return window.getComputedStyle(arguments[0]).boxSizing", first_cell)

    # Print the box-sizing value
    print(f"The box-sizing value of the first cell in the budget table is: {box_sizing_style}")

    # Check if the box-sizing value is 'border-box'
    if box_sizing_style == 'border-box':
        print("The box-sizing feature is working as expected with the value 'border-box'.")
    else:
        print("The box-sizing feature is not working as expected. It should be 'border-box'.")

finally:
    # Close the browser
    driver.quit()