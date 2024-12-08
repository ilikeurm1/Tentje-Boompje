# region allowed to touch
# Field dims
DIMENSION: int = 8

# Misc
fps_max: float = 60 # 0 for no limit
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
