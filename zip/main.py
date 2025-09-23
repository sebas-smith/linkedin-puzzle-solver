import math
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium_fetch import get_ordered_cells
from selenium_fetch import get_walls
from grid_utils import build_grid
from alg import find_path
from mousemover import drag_solution

options = Options()
options.add_argument(r"--user-data-dir=C:\Users\sebeg\AppData\Local\Microsoft\Edge\User Data")
options.add_argument(r"--profile-directory=Profile 1")  # your already-logged-in profile

driver = webdriver.Edge(options=options)

driver.get("https://www.linkedin.com/games/zip")
driver.implicitly_wait(5)

# wait until at least one cell is loaded
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-cell-idx]'))
)

ordered_cells = get_ordered_cells(driver)
sidelength = int(math.isqrt(len(ordered_cells)))
walls = get_walls(driver, sidelength)
grid = build_grid(ordered_cells)
solution = find_path(grid, walls)
drag_solution(driver, solution, ordered_cells)

input("Press Enter to close browser...")
driver.quit()

