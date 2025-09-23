import pyautogui

def drag_solution(driver, solution, ordered_cells, speed=50.0):
    """
    Drag through the solution path using PyAutoGUI with corrected screen coordinates.
    """
    pyautogui.PAUSE = 0.01
    side = int(len(ordered_cells) ** 0.5)
    cell_map = {(idx // side, idx % side): element for idx, _, element in ordered_cells}

    first_element = cell_map[solution[0]]
    rect = driver.execute_script("""
        const r = arguments[0].getBoundingClientRect();
        return {
            x: r.left,
            y: r.top,
            width: r.width,
            height: r.height,
            scrollX: window.scrollX,
            scrollY: window.scrollY,
            outerHeight: window.outerHeight,
            innerHeight: window.innerHeight
        };
    """, first_element)

    browser_offset_x = driver.execute_script("return window.screenX;")
    browser_offset_y = driver.execute_script("return window.screenY;")

    # Calculate browser chrome (toolbar) height
    chrome_height = rect["outerHeight"] - rect["innerHeight"]

    # Calculate first cell center with chrome adjustment
    start_x = browser_offset_x + rect['x'] + rect['scrollX'] + rect['width'] / 2
    start_y = browser_offset_y + chrome_height + rect['y'] + rect['scrollY'] + rect['height'] / 2

    cell_width = rect['width']
    cell_height = rect['height']

    pyautogui.moveTo(start_x, start_y, duration=0.1 / speed)
    pyautogui.leftClick()

    prev_r, prev_c = solution[0]
    for r, c in solution[1:]:
        dx = (c - prev_c) * cell_width
        dy = (r - prev_r) * cell_height
        pyautogui.moveRel(dx, dy, duration=0.02 / speed)
        pyautogui.leftClick()
        prev_r, prev_c = r, c

