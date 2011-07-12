import os.path
import numpy
import plac

@plac.annotations(
    root_path = ("path to output directory"),
    #cnf_path = ("path to CNF to be split"),
    variables = ("number of variables on which to split", "positional", None, int),
    splits = ("number of random splits to generate", "positional", None, int),
    )
def main(root_path, variables, splits):
    """Generate a CNF encoding of a grid-coloring problem."""

    # read the initial CNF
    import color_cnf

    (N, raw_clauses) = color_cnf.DirectEncoding().encode(4, 22, 17)
    selected = sorted(xrange(N), key = lambda _: numpy.random.rand())[:variables]

    for i in xrange(splits):
        fixed = []

        for v in selected:
            fixed.append([v + 1 if numpy.random.randint(2) else -v - 1])

        out_path = os.path.join(root_path, "22x17.c4.split{0}.cnf".format(i))

        with open(out_path, "w") as out_file:
            color_cnf.write_cnf(out_file, raw_clauses + fixed, N)

        print "wrote split", i, "to", out_path

if __name__ == "__main__":
    plac.call(main)

