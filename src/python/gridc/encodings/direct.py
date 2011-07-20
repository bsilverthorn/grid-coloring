"""@author: Bryan Silverthorn"""

import gridc

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

@gridc.named_encoding
class DirectEncoding(object):
    name = "direct"

    def encode(self, grid):
        # generate variable numbers
        variables = DirectEncodingVariables(grid)

        # generate cell constraints
        #clauses = [[(0, 0, 0, True)]]
        clauses = []

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

