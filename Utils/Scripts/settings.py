# Debug
DEBUG: bool = True

# region main

# Field dims
DIMENSION: int = 8

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

# Misc
fps_max: int = 0 # 0 for 1000 (max)

# endregion