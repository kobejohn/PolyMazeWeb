import random
import urllib2

import polymaze


# easy access to supershapes
_supershapes = tuple(polymaze.SUPERSHAPES_DICT.items())


class TextMaze(object):
    DEFAULT_TEXT = '.'
    DEFAULT_COMPLEXITY = 1
    TEXT_MAX = 10
    COMPLEXITY_MIN, COMPLEXITY_MAX = 1, 5

    def __init__(self, text=None, complexity=None):
        """Create and store a maze object."""
        # consider default values
        text = text or self.DEFAULT_TEXT
        complexity = complexity or self.DEFAULT_COMPLEXITY

        # cast everything if possible
        text = unicode(text)
        complexity = float(complexity)

        # modify the text to match the PolyMaze specification
        # (polymaze expects literal \n to indicate newlines)
        text = text.replace('\n', r'\n')
        text = urllib2.unquote(text)

        # create and store the maze object
        supershape_name, supershape = random.choice(_supershapes)
        grid = polymaze.PolyGrid(supershape=supershape)
        grid.create_string(text, complexity=complexity)
        maze = polymaze.Maze(grid)
        self.maze = maze

    def generate_image(self):
        image = self.maze.image()
        return image
