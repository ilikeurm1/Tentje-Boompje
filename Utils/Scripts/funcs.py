# region Imports

import numpy as np
import random

# endregion

# region Helper functions
def get_neighbors(pos: tuple[int, int], k: int, filter: bool = False) -> list[tuple[int, int]]:
    """A function that returns all the surrounding positions of a given position. For all the positions that are out of the list it sets those to 'None'.

    Args:
        pos (tuple[int, int]): The position of the element we want the neighbors.
        k (int, 4 or 8): The amount of surrounding positions to return. (see example below)
        filter (bool, optional): If True, the function will filter out the out of bound indexes. Defaults to False.

    Returns:
        neighbors (list[tuple[int, int] | None]): The (un)filtered list of surrounding positions.

    """

    x = pos[0]
    y = pos[1]

    neighbors = [
        (x - 1, y - 1)                                           # Top left
        if (x - 1 >= 1 and y - 1 >= 0 and k == 8)
        else None,

        (x - 1, y)                                               # Top
        if x - 1 >= 1
        else None,

        (x - 1, y + 1)                                           # Top right
        if (x - 1 >= 1 and y + 1 <= DIMENSION - 1 and k == 8)
        else None,

        (x, y - 1)                                               # Left
        if y - 1 >= 0
        else None,

        # (x, y)                                                 # Middel -> Not needed as it is the current position
        # if x >= 1 and y >= 1
        # else None,

        (x, y + 1)                                               # Right
        if y + 1 <= DIMENSION - 1
        else None,

        (x + 1, y - 1)                                           # Top left
        if x + 1 <= DIMENSION and y - 1 >= 0 and k == 8
        else None,

        (x + 1, y)                                               # Bottom
        if x + 1 <= DIMENSION
        else None,

        (x + 1, y + 1)                                           # Bottom right
        if x + 1 <= DIMENSION and y + 1 <= DIMENSION - 1 and k == 8
        else None
    ]

    if DEBUG:
        print(f"x: {x}, y: {y}")
        print(f"Filter: {filter}")
        print(f"Neighbors: {neighbors}")
        print(f"Filtered: {[pos for pos in neighbors if pos]}")

    return neighbors if not filter else [pos for pos in neighbors if pos] # type: ignore

def touching_tents(board: np.ndarray, pos: tuple[int, int]) -> bool:
    """This function checks if there are any touching tents on the board.

    Args:
        board (np.ndarray): The full game board.
        pos (tuple[int, int]): The position of the tent in the ndarray.

    Returns:
        bool: Are there touching tents?
    """

    for neighbor in get_neighbors(pos, 8, True):
        # If the position is a tent a.k.a. the tents are touching
        if board[neighbor[0]][neighbor[1]] == TENT:
            return True

    return False

def pretty_print(board: np.ndarray) -> None:
    """A function that prints the board in a pretty way. But leaves the top row and far right column integers as they represent the amount of tents in the rows and columns.

    Args:
        board (np.ndarray): The board to print.
    """
    emoji_list = []
    for x in range(DIMENSION + 1):
        row = []
        for y in range(DIMENSION + 1):
            if x == 0 or y == DIMENSION:
                if x == 0 and y == DIMENSION:
                    row.append(elements[PLACEHOLDER])
                else:
                    row.append(board[x][y])
            else:
                row.append(elements[board[x][y]])
        emoji_list.append(row)

    print(np.array(emoji_list))

# endregion

# region Board generation functions
def randomly_place_tents_on_board(board: np.ndarray) -> tuple[np.ndarray, list[tuple[int, tuple[int, int], bool]]]:
    tent_positions: list[tuple[int, tuple[int, int]]] = []

    for _ in range(round(DIMENSION * 2)):
        retry_counter = 0
        while True:
            x = random.randint(1, DIMENSION)
            y = random.randint(0, DIMENSION - 1)
            if board[x][y] == EMPTY and not touching_tents(board, (x, y)):
                board[x][y] = TENT
                tent_positions.append((TENT, (x, y), False))
                break

            if retry_counter > DIMENSION**2: # try max #cells_on_board times to place a tent
                break

            if retry_counter in [round(DIMENSION ** 2 / 10 * i) for i in range(1, 11)]: # Will print ~ every 10%
                    print(f"Retrying... (aborting: {round((retry_counter / DIMENSION ** 2) * 100)}%)")

            retry_counter += 1

    return board, tent_positions

def place_trees_on_board(board: np.ndarray) -> tuple[np.ndarray, list[tuple[int, tuple[int, int], bool]]]:
    tree_positions: list[tuple[int, tuple[int, int]]] = []

    for x in range(1, DIMENSION + 1): # for each row
        for y in range(DIMENSION): # for each column
            if board[x][y] == TENT:
                neighbors = get_neighbors((x, y), 4, True)
                random.shuffle(neighbors)
                for nx, ny in neighbors:
                    if board[nx][ny] == EMPTY:
                        board[nx][ny] = TREE
                        tree_positions.append((TREE, (nx, ny), True))
                        break
                    else:
                        print(f"Position: ({nx}, {ny}) is not empty it is: {board[nx][ny]} ({elements[board[nx][ny]]})")

    return board, tree_positions

def generate_tent_counts_cells(board: np.ndarray) -> np.ndarray:
    """Creates the top row and far right column of the board. These rows and columns contain the amount of tents in the rows and columns.

    Args:
        board (np.ndarray): the generated game board.

    Returns:
        board (np.ndarray): The finished game board. :)
    """
    # Step 1: Generate the far right column (x-axis)
    for x in range(1, DIMENSION + 1):
        counter = sum(1 for y in range(DIMENSION) if board[x][y] == TENT)
        board[x][DIMENSION] = counter

    # Step 2: Generate the top row (y-axis)
    for y in range(DIMENSION):
        counter = sum(1 for x in range(1, DIMENSION + 1) if board[x][y] == TENT)
        board[0][y] = counter

    # Step 3: Set the top right corner to a space
    board[0][DIMENSION] = PLACEHOLDER

    return board

def set_grass(board: np.ndarray) -> np.ndarray:
    for y in range(1, DIMENSION + 1): # For every row
        for x in range(DIMENSION): # Go through every column
            pretty_print(board)

            if board[0][x] == 0 or board[y][DIMENSION] == 0: # If the cell is in a collumn or a row with 0 tents
                if board[y][x] != TREE:
                    board[y][x] = GRASS

            else: # for the rest of the rows
                    if board[y][x] == EMPTY:
                        trees_spaces = get_neighbors((y, x), 4, True)
                        for nx, ny in trees_spaces:
                            if board[nx][ny] == TREE:
                                break
                        else:
                            board[y][x] = GRASS

    return board

def delete_tents(board: np.ndarray) -> np.ndarray:
    for x in range(1, DIMENSION + 1):
        for y in range(DIMENSION):
            if board[x][y] == TENT:
                board[x][y] = EMPTY
    return board

# endregion

# region Main generation function
def CREATE_VALID_GAME() -> tuple[np.ndarray, list[tuple[int, tuple[int, int], bool]]]:
    """This function creates a valid game board.

    Args:
        init_board (np.ndarray): The initial game board.

    Returns:
        board, game_board_positions (np.ndarray, list[tuple[int, tuple[int, int]]]): The finished game board and the positions of the tents and trees expressed in indices.
    """

    # Define the list that will hold the positions of the tents and trees
    game_board_positions: list[tuple[int, tuple[int, int], bool]] = []

    # Step 1: Initialize the board
    # Board needs to be 1 bigger than the DIMENSION to hold the info about how many tents are in the rows and columns
    board = np.array([[EMPTY for _ in range(DIMENSION + 1)] for _ in range(DIMENSION + 1)])

    # Step 2: Randomly place tents on the board
    board, tent_positions = randomly_place_tents_on_board(board)

    # Step 3: Place trees on the board
    board, tree_positions = place_trees_on_board(board)

    # Step 4: Generate the tent counts for the cells
    board = generate_tent_counts_cells(board)

    # Step 5: Set all the places where there can't be anything to grass
    board = set_grass(board)

    # Print the board to see if its correct
    if DEBUG:
        pretty_print(board)

    # Step 6: Delete the tents so the game is playable
    board = delete_tents(board)

    game_board_positions.extend(tent_positions)
    game_board_positions.extend(tree_positions)

    # return board
    return board, game_board_positions

# endregion

# Main function
def main() -> int:
    """Main utils function."""
    print("Hello from funcs.py")

    try:
        board = CREATE_VALID_GAME()
        pretty_print(board)

    except Exception as e:
        print(f"An error occurred: {e}")
        return 1

    return 0


# region misc __main__
if __name__ == "__main__":
    from settings import (
        DIMENSION,
        EMPTY,
        GRASS,
        TREE,
        TENT,
        PLACEHOLDER,
        elements,
        DEBUG,
    )
    exit_code = main()

    if exit_code != 0:
        print(
            "An error occurred.\nexit code: 1\n"
        )

    else:
        print(
            f"Program exited successfully.\nexit code: {exit_code}\n"
        )
else:
    from Utils.Scripts.settings import (
        DIMENSION,
        EMPTY,
        GRASS,
        TREE,
        TENT,
        PLACEHOLDER,
        elements,
        DEBUG
    )
    print("funcs.py imported")

# endregion
