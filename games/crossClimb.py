import time
from helpers import is_puzzle_completed

HANDLE_SELECTOR = "div.crossclimb__guess-dragger.crossclimb__guess-dragger__right[data-sortable-handle='true']"

def fill_crossClimb(page, puzzle, pause_after_move=0.3):
    
    if is_puzzle_completed(page):
        print("crossClimb already completed, skipping.")
        return
    
    """
    Bottom-up mover
    """
    
    rungs = puzzle.get("rungs", [])
    top = rungs[0]["word"]
    bottom = rungs[-1]["word"]
    
    words = ""
    for rung in rungs[1:-1]:
        word = rung["word"]
        words += word

    page.keyboard.type(f"{words}")
    
    if not rungs or len(rungs) <= 2:
        print("Nothing to move (no rungs or only fixed rungs).")
        return

    movable = [r for r in rungs[1:-1]]
    if not movable:
        print("No movable rungs found.")
        return

    target_ranks = sorted((r["solutionRungIndex"] for r in movable), reverse=True)

    placed = 0
    for rank in target_ranks:
        target_pos = len(movable) - 1 - placed

        try:
            current_idx = next(i for i, rr in enumerate(movable) if rr["solutionRungIndex"] == rank)
        except StopIteration:
            print(f"⚠️ No rung with solutionRungIndex={rank} found; skipping.")
            continue

        if current_idx == target_pos:
            print(f"✅ Already at target spot: rank={rank} (idx {current_idx})")
            placed += 1
            continue

        handles = page.query_selector_all(HANDLE_SELECTOR)
        if not handles:
            print("⚠️ No handles found on page")
            return

        src_idx = min(current_idx, len(handles) - 1)
        dst_idx = min(target_pos, len(handles) - 1)

        src_box = handles[src_idx].bounding_box()
        dst_box = handles[dst_idx].bounding_box()
        if not src_box or not dst_box:
            print(f"⚠️ Could not get bounding boxes; skipping rank={rank}")
            continue

        print(f"🔄 Moving rung with solutionRungIndex={rank}: current_idx={current_idx} → target_pos={target_pos}")

        # Calculate start and end positions
        start_x = src_box["x"] + src_box["width"] / 2
        start_y = src_box["y"] + src_box["height"] / 2
        end_x = dst_box["x"] + dst_box["width"] / 2
        end_y = dst_box["y"] + dst_box["height"] * 1  # slight overshoot

        # Very slow smooth drag
        page.mouse.move(start_x, start_y)
        page.mouse.down()

        steps = 15  # more steps → slower drag
        for i in range(1, steps + 1):
            t = i / steps
            intermediate_x = start_x + (end_x - start_x) * t
            intermediate_y = start_y + (end_y - start_y) * t
            page.mouse.move(intermediate_x, intermediate_y)
            time.sleep(0.02)  # slower step delay so movement is visible

        page.mouse.up()
        time.sleep(pause_after_move)

        # Update local state
        item = movable.pop(current_idx)
        movable.insert(target_pos, item)
        print(f"→ Local movable order now: {[r['word'] for r in movable]}")
        placed += 1

    print("✅ CrossClimb moves finished (bottom-up).")
    
    

    page.keyboard.type(top)
    page.keyboard.type(bottom)
