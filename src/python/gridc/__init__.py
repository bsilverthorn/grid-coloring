"""@author: Bryan Silverthorn"""

import cargo

logger = cargo.get_logger(__name__)

_encodings_by_name = {}

def named_encoding(class_):
    _encodings_by_name[class_.name] = class_()

    logger.info("registered encoding %s", class_.name)

    return class_

def encoding(name):
    return _encodings_by_name[name]

class Grid(object):
    """Instance of the grid-coloring problem."""

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.colors = 4

    def is_coloring(self, coloring):
        """Is the specified coloring a valid coloring?"""

        for x0 in xrange(self.width):
            for y0 in xrange(self.height):
                for x1 in xrange(x0 + 1, self.width):
                    for y1 in xrange(y0 + 1, self.height):
                        if coloring[x0, y0] == coloring[x0, y1] == coloring[x1, y0] == coloring[x1, y1]:
                            return False

        return True

from . import encodings

