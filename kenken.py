from functools import reduce
from random import choice, randint, random, shuffle

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


def make_new_random_board(board_size):
    # Create a square matrix of board_size 'board_size' with elements [1...board_size] according to kenken rules.
    board = [[((i + j) % board_size) + 1 for i in range(board_size)]
             for j in range(board_size)]

    # Shuffle the board by rows and columns to get random and valid kenken board.
    for _ in range(board_size):
        shuffle(board)

    # More shuffling
    for c1 in range(board_size):
        for c2 in range(board_size):
            if random() > 0.5:
                for r in range(board_size):
                    board[r][c1], board[r][c2] = board[r][c2], board[r][c1]

    # Initialize the 'uncaged' set with all cell coordinates.
    board = {(j + 1, i + 1): board[i][j]
             for i in range(board_size) for j in range(board_size)}

    # Sort the 'uncaged' set according to row major order. [x] coordinate
    uncaged = sorted(board.keys(), key=lambda var: var[1])

    cliques = []

    while uncaged:
        cliques.append([])
        csize = randint(1, 4)
        cell = uncaged[0]
        uncaged.remove(cell)
        cliques[-1].append(cell)

        for _ in range(csize - 1):
            # Randomly visit at most 'clique-size' 'uncaged' adjacent cells
            adjs = [
                other for other in uncaged if is_two_cells_are_adjacent(cell, other)]
            # Randomly choose an adjacent cell
            cell = choice(adjs) if adjs else None
            # If there is no adjacent cell, then the clique is complete
            if not cell:
                break
            # Add the cell to the clique and remove it from the 'uncaged' set
            uncaged.remove(cell)
            cliques[-1].append(cell)
        # If the clique is complete and its size == 1,
        # then there is no operation to be performed
        csize = len(cliques[-1])
        if csize == 1:
            cell = cliques[-1][0]
            cliques[-1] = ((cell, ), '=', board[cell])
            continue
        # If the clique is complete and its size == 2,
        elif csize == 2:
            # if the two elements of the clique can be divided without a remainder
            # then the operation is set to division and the target is the quotient
            fst, snd = cliques[-1][0], cliques[-1][1]
            if board[fst] / board[snd] > 0 and not board[fst] % board[snd]:
                operator = "/"
            # otherwise, the operation is set to subtraction
            # and the target is the difference of the elements
            else:
                operator = "-"
        # Otherwise, randomly choose an operation between addition and multiplication.
        else:
            operator = choice("+*")
        # The target of the operation is the result of applying the decided
        target = reduce(select_operation(operator), [
                        board[cell] for cell in cliques[-1]])
        # Add the operation to the clique
        cliques[-1] = (tuple(cliques[-1]), operator, int(target))
    # Return the cliques
    return board_size, cliques
