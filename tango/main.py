import math
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium_fetch import get_positions


options = Options()
options.add_argument(r"--user-data-dir=C:\Users\sebeg\AppData\Local\Microsoft\Edge\User Data")
options.add_argument(r"--profile-directory=Profile 1")  # your already-logged-in profile

driver = webdriver.Edge(options=options)

driver.get("https://www.linkedin.com/games/tango")
driver.implicitly_wait(5)

# wait until at least one cell is loaded
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-cell-idx]'))
)

print(get_positions(driver))

input("Press Enter to close browser...")
driver.quit()

