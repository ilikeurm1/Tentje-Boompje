# region allowed to touch

# Board dimensions
DIMENSION: int = 8

# Set all the places where there cant be a tent to grass (True) or leave them empty (False)
PREPLACE_GRASS: bool = True

# Misc
fps_max: float = 60 # 0 for no limit
lives: int = 3

# endregion

# region dont touch
# Field elements
EMPTY: int = -1
GRASS: int = 0
TREE: int = 1
TENT: int = 2
PLACEHOLDER: int = 10

elements = {
    EMPTY: "💧",
    GRASS: "🍏",
    TREE: "🌳",
    TENT: "⛺",
    PLACEHOLDER: "🪧"
}

# Debug
DEBUG: bool = False

# endregion
