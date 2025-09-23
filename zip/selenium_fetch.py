from selenium.webdriver.common.by import By
import math

def get_ordered_cells(driver):
    # get all cell containers
    cells = driver.find_elements(By.CSS_SELECTOR, 'div[data-cell-idx]')

    # get all filled number divs at once
    numbered_divs = driver.find_elements(By.CSS_SELECTOR, 'div[data-cell-content="true"]')
    
    # map from parent cell idx to the number
    idx_to_number = {}
    for num_div in numbered_divs:
        parent = num_div.find_element(By.XPATH, './..')  # parent div
        idx = int(parent.get_attribute("data-cell-idx"))
        idx_to_number[idx] = int(num_div.text)

    ordered_cells = []
    for cell in cells:
        idx = int(cell.get_attribute("data-cell-idx"))
        value = idx_to_number.get(idx)  # None if empty
        ordered_cells.append((idx, value, cell))  # include element!

    return ordered_cells


def get_walls(driver, side_length):
    """
    Returns a set of blocked moves as ((r, c), (rr, cc)) pairs
    suitable for direct use in your DFS algorithm.
    
    side_length: int, width/height of the grid
    """
    wall_divs = driver.find_elements(
        By.CSS_SELECTOR,
        "div.a5f9ca12._283f0f13._34dddcc8._9c2832ad._5a745179"
    )

    walls = set()
    for wall in wall_divs:
        parent_cell = wall.find_element(By.XPATH, "./ancestor::div[@data-cell-idx]")
        cell_idx = int(parent_cell.get_attribute("data-cell-idx"))
        r, c = divmod(cell_idx, side_length)

        wall_class = wall.get_attribute("class")
        if "_77e05ace" in wall_class:
            # right wall blocks (r, c) -> (r, c+1) and vice versa
            walls.add(((r, c), (r, c+1)))
            walls.add(((r, c+1), (r, c)))
        elif "_441dd5bf" in wall_class:
            # down wall blocks (r, c) -> (r+1, c) and vice versa
            walls.add(((r, c), (r+1, c)))
            walls.add(((r+1, c), (r, c)))

    return walls



if __name__ == "__main__":
    from selenium import webdriver
    from selenium.webdriver.edge.options import Options
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.common.by import By
    from selenium_fetch import get_ordered_cells
    from grid_utils import build_grid
    from alg import find_path

    options = Options()
    options.add_argument(r"--user-data-dir=C:\Users\sebeg\AppData\Local\Microsoft\Edge\User Data")
    options.add_argument(r"--profile-directory=Profile 1")  # your already-logged-in profile

    driver = webdriver.Edge(options=options)

    driver.get("https://www.linkedin.com/games/zip")
    driver.implicitly_wait(5)

    # wait until at least one cell is loaded
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-cell-idx]')))
        
        
    ordered_cells = get_ordered_cells(driver)
    sidelength = int(math.isqrt(len(ordered_cells)))
    walls = get_walls(driver, sidelength)
    print(f"walls: {walls}")