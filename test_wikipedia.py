import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

@pytest.fixture(params=["chrome", "edge"], scope="class")
def driver_init(request):
    if request.param == "chrome":
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    elif request.param == "edge":
        driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
    
    request.cls.driver = driver
    yield
    driver.quit()

@pytest.mark.usefixtures("driver_init")
class TestWikipedia:
    def test_wikipedia_logo_size(self):
        self.driver.get('https://en.wikipedia.org/wiki/NASA')
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#p-logo > a')))
        
        logo = self.driver.find_element(By.CSS_SELECTOR, '#p-logo > a')
        logo_width = logo.size['width']
        logo_height = logo.size['height']
        assert logo_width == 160, f"Expected logo width to be 160 but got {logo_width}"
        assert logo_height == 160, f"Expected logo height to be 160 but got {logo_height}"
        logo.screenshot(f'{self.driver.name}_logo_screenshot.png')

    def test_wikipedia_body_background_color(self):
        self.driver.get('https://en.wikipedia.org/wiki/NASA')
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body')))
        
        body = self.driver.find_element(By.CSS_SELECTOR, 'body')
        body_color = body.value_of_css_property('background-color')
        assert body_color == 'rgba(248, 249, 250, 1)', f"Expected background color to be rgba(248, 249, 250, 1) but got {body_color}"

    def test_wikipedia_table_box_sizing(self):
        self.driver.get('https://en.wikipedia.org/wiki/NASA')
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'table.wikitable')))
        
        table = self.driver.find_element(By.CSS_SELECTOR, 'table.wikitable')
        table_box_sizing = table.value_of_css_property('box-sizing')
        assert table_box_sizing == 'border-box', f"Expected table box-sizing to be border-box but got {table_box_sizing}"
        table.screenshot(f'{self.driver.name}_table_screenshot.png')

    def test_wikipedia_link_font(self):
        self.driver.get('https://en.wikipedia.org/wiki/NASA')
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a')))
        
        link = self.driver.find_element(By.CSS_SELECTOR, 'a')
        font_family = link.value_of_css_property('font-family')
        font_size = link.value_of_css_property('font-size')
        assert 'sans-serif' in font_family.lower(), f"Expected font family to include 'Sans Serif' but got {font_family}"
        assert font_size == '16px', f"Expected font size to be 16px but got {font_size}"

if __name__ == "__main__":
    pytest.main(['-v', '--html=report.html'])
