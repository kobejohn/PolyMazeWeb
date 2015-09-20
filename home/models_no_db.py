import random
import urllib2

from django.core.exceptions import ValidationError

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
        text = text.strip() or self.DEFAULT_TEXT  # 100% white space yields a default also
        complexity = self.DEFAULT_COMPLEXITY if complexity is None else complexity

        # cast everything if possible
        text = unicode(text)
        complexity = float(complexity)

        # modify the text to match the PolyMaze specification
        # (polymaze expects literal \n to indicate newlines)
        text = text.replace('\n', r'\n')
        text = urllib2.unquote(text)

        # validate
        self._validate_text(text)
        self._validate_complexity(complexity)

        # store
        self._text = text
        self._complexity = complexity

    def generate_image(self):
        return self._maze.image()

    def _validate_text(self, text):
        """Raise ValidationError if not None (default) or some valid value."""
        if text is None:
            return
        if not (0 < len(text) <= self.TEXT_MAX):
            raise ValidationError

    def _validate_complexity(self, complexity):
        """Raise ValidationError if not None (default) or some valid value."""
        if complexity is None:
            return
        if not (self.COMPLEXITY_MIN <= complexity <= self.COMPLEXITY_MAX):
            raise ValidationError

    @property
    def _maze(self):
        """Lazy creation of maze object."""
        try:
            return self.__maze
        except AttributeError:
            pass
        # create and store the maze object
        supershape_name, supershape = random.choice(_supershapes)
        grid = polymaze.PolyGrid(supershape=supershape)
        grid.create_string(self._text, complexity=self._complexity)
        self.__maze = polymaze.Maze(grid)
        return self.__maze
