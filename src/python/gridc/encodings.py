import borg
import numpy

by_name = {}

def named_encoding(class_):
    by_name[class_.name] = class_()

    return class_

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

class DirectEncodingVariables(object):
    def __init__(self, grid):
        self.of_cnf = {}
        self.of_grid = {}

        for x in xrange(grid.width):
            for y in xrange(grid.height):
                for c in xrange(4):
                    v = len(self.of_cnf)

                    self.of_cnf[(c, x, y)] = v + 1
                    self.of_grid[v + 1] = (c, x, y)

@named_encoding
class DirectEncoding(object):
    name = "direct"

    def encode(self, grid):
        # generate variable numbers
        variables = DirectEncodingVariables(grid)

        # generate cell constraints
        clauses = [[(0, 0, 0, True)]]

        for x in xrange(grid.width):
            for y in xrange(grid.height):
                clauses.append([(c, x, y, True) for c in xrange(4)])

                for c in xrange(4):
                    for d in xrange(c + 1, 4):
                        clauses.append([(c, x, y, False), (d, x, y, False)])

        # generate rectangle constraints
        for x0 in xrange(grid.width):
            for y0 in xrange(grid.height):
                for x1 in xrange(x0 + 1, grid.width):
                    for y1 in xrange(y0 + 1, grid.height):
                        for c in xrange(4):
                            clauses.append([
                                (c, x0, y0, False),
                                (c, x0, y1, False),
                                (c, x1, y0, False),
                                (c, x1, y1, False),
                                ])

        # build CNF
        def literal((c, x, y, p)):
            if p:
                return variables.of_cnf[(c, x, y)]
            else:
                return -variables.of_cnf[(c, x, y)]

        return \
            borg.domains.sat.instance.SAT_Instance.from_clauses(
                [map(literal, clause) for clause in clauses],
                len(variables.of_cnf),
                )

    def decode(self, grid, answer):
        """Return a coloring given a grid and a solution to the CNF."""

        variables = DirectEncodingVariables(grid)
        coloring = numpy.ones((grid.width, grid.height), int) * -1

        for literal in answer:
            if literal > 0:
                (c, x, y) = variables.of_grid[literal]

                assert coloring[x, y] == -1

                coloring[x, y] = c

        return coloring

class LogEncodingVariables(object):
    def __init__(self, grid):
        self.of_cnf = {}
        self.of_grid = {}

        for x in xrange(grid.width):
            for y in xrange(grid.height):
                for b in xrange(2):
                    v = len(self.of_cnf)

                    self.of_cnf[(x, y, b)] = v + 1
                    self.of_grid[v + 1] = (x, y, b)

    def __len__(self):
        return len(self.of_cnf)

    def to_cnf(self, x, y, b):
        return self.of_cnf[(x, y, b)]

    def to_cnf_literal(self, x, y, b, p):
        v = self.to_cnf(x, y, b)

        return v if p else -v

@named_encoding
class LogEncoding(object):
    name = "log"

    def encode(self, grid):
        variables = LogEncodingVariables(grid)

        def rclause(x0, y0, x1, y1, b0, b1):
            grid_literals = [
                (x0, y0, 0, b0),
                (x0, y0, 1, b1),
                (x0, y1, 0, b0),
                (x0, y1, 1, b1),
                (x1, y0, 0, b0),
                (x1, y0, 1, b1),
                (x1, y1, 0, b0),
                (x1, y1, 1, b1),
                ]

            return [variables.to_cnf_literal(x, y, b, p) for (x, y, b, p) in grid_literals]

        clauses = []

        for x0 in xrange(grid.width):
            for y0 in xrange(grid.height):
                for x1 in xrange(x0 + 1, grid.width):
                    for y1 in xrange(y0 + 1, grid.height):
                        clauses.append(rclause(x0, y0, x1, y1, True, True))
                        clauses.append(rclause(x0, y0, x1, y1, True, False))
                        clauses.append(rclause(x0, y0, x1, y1, False, True))
                        clauses.append(rclause(x0, y0, x1, y1, False, False))

        return \
            borg.domains.sat.instance.SAT_Instance.from_clauses(
                clauses,
                len(variables),
                )

    def decode(self, grid, answer):
        """Return a coloring given a grid and a solution to the CNF."""

        variables = LogEncodingVariables(grid)
        coloring = numpy.ones((grid.width, grid.height), int) * -1

        for x in xrange(grid.width):
            for y in xrange(grid.height):
                v0 = variables.to_cnf(x, y, 0) - 1
                v1 = variables.to_cnf(x, y, 1) - 1

                p0 = 1 if answer[v0] > 0 else 0
                p1 = 1 if answer[v1] > 0 else 0

                coloring[x, y] = p0 * 1 + p1 * 2

        return coloring

