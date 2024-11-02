# region Imports
import numpy as np
import random
# endregion

# region Helper functions
def get_neighbours(
    pos: tuple[int, int], k: int, filter: bool = False
    ) -> list[tuple[int, int]]:
    """A function that returns all the surrounding positions of a given position. For all the positions that are out of the list it sets those to 'None'.

    Args:
        pos (tuple[int, int]): The position of the element we want the neighbours.
        k (int, 4 or 8): The amount of surrounding positions to return. (see example below)
        filter (bool, optional): If True, the function will filter out the out of bound indexes. Defaults to False.

    Returns:
        neighbours (list[tuple[int, int] | None]): The (un)filtered list of surrounding positions.

    """

    x = pos[0]
    y = pos[1]

    neighbours = [
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

    # if DEBUG:
    #     print(f"x: {x}, y: {y}")
    #     print(f"Filter: {filter}")
    #     print(f"Neighbours: {neighbours}")
    #     print(f"Filtered: {[pos for pos in neighbours if pos]}")

    return neighbours if not filter else [pos for pos in neighbours if pos] # type: ignore

def touching_tents(board: np.ndarray, pos: tuple[int, int]) -> bool:
    """This function checks if there are any touching tents on the board.

    Args:
        board (np.ndarray): The full game board.
        pos (tuple[int, int]): The position of the tent in the ndarray.

    Returns:
        bool: Are there touching tents?
    """

    for surrounding_pos in get_neighbours(pos, 8, True):
        # If the position is a tent a.k.a. the tents are touching
        if board[surrounding_pos[0]][surrounding_pos[1]] == TENT:
            return True

    return False

def pretty_print(board: np.ndarray) -> None:
    """A function that prints the board in a pretty way. But leaves the top row and far right column integers as they represent the amount of tents in the rows and columns.

    Args:
        board (np.ndarray): The board to print.
    """
    l = []
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
        l.append(row)

    print(np.array(l))

# endregion

# region Board generation functions
def randomly_place_tents_on_board(board: np.ndarray) -> np.ndarray:
    for _ in range(DIMENSION):
        while True:
            x = random.randint(1, DIMENSION)
            y = random.randint(0, DIMENSION - 1)
            if board[x][y] == EMPTY and not touching_tents(board, (x, y)):
                board[x][y] = TENT
                break
    return board

def place_trees_on_board(board: np.ndarray) -> np.ndarray:
    for x in range(1, DIMENSION + 1): # for each row
        for y in range(DIMENSION): # for each column
            if board[x][y] == TENT:
                neighbours = get_neighbours((x, y), 4, True)
                random.shuffle(neighbours)
                for nx, ny in neighbours:
                    if board[nx][ny] == EMPTY:
                        board[nx][ny] = TREE
                        break
                    else:
                        print(f"Position: {nx, ny} is not empty it is: {board[nx][ny]} ({elements[board[nx][ny]]})")

    return board

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

# endregion

# region Main generation function
def CREATE_VALID_GAME() -> np.ndarray:
    """This function creates a valid game board.

    Args:
        init_board (np.ndarray): The initial game board.

    Returns:
        np.ndarray: The valid game board.
    """

    # Step 1: Initialize the board
    # Board needs to be 1 bigger than the DIMENSION to hold the info about how many tents are in the rows and columns
    board = np.array([[EMPTY for _ in range(DIMENSION + 1)] for _ in range(DIMENSION + 1)])

    # Step 2: Randomly place tents on the board
    board = randomly_place_tents_on_board(board) 
    

    # Step 3: Place trees on the board
    board = place_trees_on_board(board)
    
    # Step 4: Generate the tent counts for the cells
    board = generate_tent_counts_cells(board)

    # return board
    return board

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
        TREE,
        GRASS,
        TENT,
        PLACEHOLDER,
        elements,
        DEBUG,
    )
    exit_code = main()

    if exit_code != 0:
        print(
            f"An error occurred.\nexit code: 0\n"
        )

    else:
        print(
            f"Program exited successfully.\nexit code: {exit_code}\n"
        )
else:
    from Utils.Scripts.settings import (
        DIMENSION,
        EMPTY,
        TREE,
        GRASS,
        TENT,
        PLACEHOLDER,
        elements,
        DEBUG
    )
    print("funcs.py imported")
# endregion
