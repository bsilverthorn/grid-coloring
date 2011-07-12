import os.path
import plac

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
    def decode(self):
        pass

@plac.annotations(
    root_path = ("path to output directory"),
    min_width = ("min width in cells", "positional", None, int),
    max_width = ("max width in cells", "positional", None, int),
    min_height = ("height in cells", "positional", None, int),
    max_height = ("height in cells", "positional", None, int),
    colors = ("number of colors", "option", "c", int),
    )
def main(root_path, min_width, max_width, min_height, max_height, colors = 4):
    """Generate a CNF encoding of a grid-coloring problem."""

    for width in xrange(min_width, max_width + 1):
        for height in xrange(min_height, max_height + 1):
            out_path = os.path.join(root_path, "{0}x{1}.c{2}.cnf".format(width, height, colors))

            with open(out_path, "w") as out_file:
                write_constraints(out_file, colors, width, height)

if __name__ == "__main__":
    plac.call(main)

