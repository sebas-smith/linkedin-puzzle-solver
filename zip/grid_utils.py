import math

def build_grid(ordered_cells):
    ordered_cells = sorted(ordered_cells, key=lambda x: x[0])
    flat_list = [val for _, val, _ in ordered_cells]
    L = len(flat_list)
    side = int(math.isqrt(L))
    return [flat_list[i*side:(i+1)*side] for i in range(side)]