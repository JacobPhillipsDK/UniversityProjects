from WindowDraw import DrawWindow

# --- Global constants ---

# Dictionary for Colours!
colour_dict = {
    "RED": (255, 0, 0),
    "BLACK": (0, 0, 0),
    "WHITE": (255, 255, 255),
    "GREEN": (0, 255, 0),
    "BLUE": (0, 0, 255)
}
# Define constants for the screen width and height
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)


# --- Global constants ENDS HERE ---


def main():
    DrawWindow(pygame_screen_size=SCREEN_SIZE, bg_colour=colour_dict.get("WHITE"), grid_colour=colour_dict.get("RED"),
               node_grid_size=600)


if __name__ == '__main__':
    main()
