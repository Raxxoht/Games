from pygame.math import Vector2


# Screen size
window_width = 800
window_height = 500

# Player settings
player_size = Vector2(15,20)
player_speed = 1
player_color = (255,255,255)
speedStopMargin = 0.01

# Physics
friction = 0.05
fps = 10
target_fps = 30
dt = 0