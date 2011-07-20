"""@author: Bryan Silverthorn"""

import gridc

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

@gridc.named_encoding
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

