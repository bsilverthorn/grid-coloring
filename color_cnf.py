import plac

def write_constraints(out_file, colors, width, height):
    # generate variable numbers
    variables = {}

    for x in xrange(width):
        for y in xrange(height):
            for c in xrange(colors):
                variables[(c, x, y)] = len(variables) + 1

    # generate cell constraints
    clauses = [[(0, 0, 0, True)]]

    for x in xrange(width):
        for y in xrange(height):
            clauses.append([(c, x, y, True) for c in xrange(colors)])

            for c in xrange(colors):
                for d in xrange(c + 1, colors):
                    clauses.append([(c, x, y, False), (d, x, y, False)])

    # generate rectangle constraints
    for x0 in xrange(width):
        for y0 in xrange(height):
            for x1 in xrange(x0 + 1, width):
                for y1 in xrange(y0 + 1, height):
                    for c in xrange(colors):
                        clauses.append([
                            (c, x0, y0, False),
                            (c, x0, y1, False),
                            (c, x1, y0, False),
                            (c, x1, y1, False),
                            ])

    # write CNF
    def literal((c, x, y, p)):
        if p:
            return str(variables[(c, x, y)])
        else:
            return "-" + str(variables[(c, x, y)])

    out_file.write("c filling a {0}x{1} grid with {2} colors\n".format(width, height, colors))
    out_file.write("p cnf {0} {1}\n".format(len(variables), len(clauses)))

    for clause in clauses:
        out_file.write(" ".join(map(literal, clause)))
        out_file.write(" 0\n")

@plac.annotations(
    out_path = ("path to output file"),
    colors = ("number of colors", "option", "c", int),
    width = ("width in cells", "positional", None, int),
    height = ("height in cells", "positional", None, int),
    )
def main(out_path, width, height, colors = 4):
    """Generate a CNF encoding of a grid-coloring problem."""

    with open(out_path, "w") as out_file:
        write_constraints(out_file, colors, width, height)

if __name__ == "__main__":
    plac.call(main)

