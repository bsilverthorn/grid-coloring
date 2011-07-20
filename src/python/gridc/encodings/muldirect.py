"""@author: Bryan Silverthorn"""

import gridc
import borg

class MuldirectEncodingVariables(object):
    def __init__(self, grid):
        self.grid = grid

    def __len__(self):
        return self.grid.width * self.grid.height * 4

    def to_cnf(self, (x, y, c)):
        return 1 + x * 4 + y * self.grid.width * 4 + c

    def to_cnf_literal(self, g):
        (x, y, c, p) = g

        v = self.to_cnf((x, y, c))

        return v if p else -v

@gridc.named_encoding
class MuldirectEncoding(object):
    name = "muldirect"

    def encode(self, grid):
        # generate variable numbers
        variables = MuldirectEncodingVariables(grid)

        # generate cell constraints
        clauses = []

        for x in xrange(grid.width):
            for y in xrange(grid.height):
                grid_literals = [(x, y, c, True) for c in xrange(4)]

                clauses.append(map(variables.to_cnf_literal, grid_literals))

        # generate rectangle constraints
        for x0 in xrange(grid.width):
            for y0 in xrange(grid.height):
                for x1 in xrange(x0 + 1, grid.width):
                    for y1 in xrange(y0 + 1, grid.height):
                        for c in xrange(4):
                            grid_literals = [
                                (x0, y0, c, False),
                                (x0, y1, c, False),
                                (x1, y0, c, False),
                                (x1, y1, c, False),
                                ]

                            clauses.append(map(variables.to_cnf_literal, grid_literals))

        # XXX this in fact implements only the muldirect encoding---need to
        # weaken later constraints (and keep around the muldirect encoding in a
        # separate class)

        # build CNF
        return \
            borg.domains.sat.instance.SAT_Instance.from_clauses(
                clauses,
                len(variables),
                )

    def decode(self, grid, answer):
        """Return a coloring given a grid and a solution to the CNF."""

        variables = MuldirectEncoding(grid)
        coloring = numpy.ones((grid.width, grid.height), int) * -1

        for x in xrange(grid.width):
            for y in xrange(grid.height):
                for c in xrange(4):
                    v = variables.to_cnf((x, y, c))

                    if coloring[x, y] >= 0:
                        break
                    elif answer[abs(v) - 1] > 0:
                        coloring[x, y] = c

        return coloring

