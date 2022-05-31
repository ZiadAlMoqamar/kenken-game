# checks if two cells are adjacent
def is_two_cells_are_adjacent(xy1, xy2):
    x1, y1 = xy1
    x2, y2 = xy2
    dx = x1 - x2
    dy = y1 - y2

    return (dx == 0 and abs(dy) == 1) or (dy == 0 and abs(dx) == 1)

# define all operations that can be performed on a kenken puzzle


def select_operation(inputOperator):
    if inputOperator == '+':
        return lambda a, b: a + b

    elif inputOperator == '-':
        return lambda a, b: a - b

    elif inputOperator == '*':
        return lambda a, b: a * b

    elif inputOperator == '/':
        return lambda a, b: a / b

    else:
        return None
