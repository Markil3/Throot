import thumby

class ObstacleSlice:
    """
    The game world is divided up into distinct "slices," where each slice is a predefined set of
    obstacles in specific positions. These slices are then put forward in random order
    """

    """
    How many units an obstacle slice is high
    """
    height=max(80, thumby.display.height * 2)
    
    def __init__(self, obstacle_map, difficulty: int):
        """
        Creates an obstacle slice

        :param obstacle_map:
            A two-dimensional list description what obstacles are here. Each tuple describes a
            single obstacle, its x, and y position, the obstacle type, the x mirror, and the y
            mirror.
        :param difficulty:
            The difficulty of the game. This influences when this slice appears.
        """
        self.obstacle_map = obstacle_map
        self.difficulty = difficulty

OBSTACLE_SLICES = [
    ObstacleSlice(
        [
            (10, 0, 0, 0, 0),
            (53, 30, 1, 0, 0),
            (5, 45, 0, 0, 0)
        ],
        0
    )
]
