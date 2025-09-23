from selenium.webdriver.common.by import By
import math

# Suns are 1 and Moons are 0

def get_positions(driver):
    # get all cell containers
    cells = driver.find_elements(By.CSS_SELECTOR, 'div[data-cell-idx]')

    # get all filled number divs at once
    suns = driver.find_elements(By.CSS_SELECTOR, 'svg[aria-label="Sun"]')
    moons = driver.find_elements(By.CSS_SELECTOR, 'svg[aria-label="Moon"]')
    
    print(f"suns: {suns}")
    print(f"moons: {moons}")
    
    
    # map from parent cell idx to the number
    initial_positions = {}
    for sun in suns:
        grandparent = sun.find_element(By.XPATH, './../..')
        idx = int(grandparent.get_attribute("data-cell-idx"))
        initial_positions[idx] = 1
    for moon in moons:
        grandparent = moon.find_element(By.XPATH, './../..')
        idx = int(grandparent.get_attribute("data-cell-idx"))
        initial_positions[idx] = 0

    return initial_positions