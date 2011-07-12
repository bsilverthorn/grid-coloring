import borg

class Grid(object):
    """Instance of the grid-coloring problem."""

    def __init__(self, colors, width, height):
        self.colors = colors
        self.width = width
        self.height = height

class DirectEncoding(object):
    def encode(self, grid):
        # generate variable numbers
        variables = {}

        for x in xrange(grid.width):
            for y in xrange(grid.height):
                for c in xrange(grid.colors):
                    variables[(c, x, y)] = len(variables) + 1

        # generate cell constraints
        clauses = [[(0, 0, 0, True)]]

        for x in xrange(grid.width):
            for y in xrange(grid.height):
                clauses.append([(c, x, y, True) for c in xrange(grid.colors)])

                for c in xrange(grid.colors):
                    for d in xrange(c + 1, grid.colors):
                        clauses.append([(c, x, y, False), (d, x, y, False)])

        # generate rectangle constraints
        for x0 in xrange(grid.width):
            for y0 in xrange(grid.height):
                for x1 in xrange(x0 + 1, grid.width):
                    for y1 in xrange(y0 + 1, grid.height):
                        for c in xrange(grid.colors):
                            clauses.append([
                                (c, x0, y0, False),
                                (c, x0, y1, False),
                                (c, x1, y0, False),
                                (c, x1, y1, False),
                                ])

        # build CNF
        def literal((c, x, y, p)):
            if p:
                return variables[(c, x, y)]
            else:
                return -variables[(c, x, y)]

        return \
            borg.domains.sat.instance.SAT_Instance.from_clauses(
                [map(literal, clause) for clause in clauses],
                len(variables),
                )

    def decode(self, grid, answer):
        """Return a coloring from a grid and a solution to the CNF."""

        pass

class LogEncoding(object):
    def encode(self, grid):
        pass

    def decode(self):
        pass

