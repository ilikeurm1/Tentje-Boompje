# region allowed to touch

# Board dimensions
DIMENSION: int = 8

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
