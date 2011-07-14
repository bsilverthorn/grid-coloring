import os.path
import plac
import gridc

@plac.annotations(
    root_path = ("path to output directory"),
    min_width = ("min width in cells", "positional", None, int),
    max_width = ("max width in cells", "positional", None, int),
    min_height = ("height in cells", "positional", None, int),
    max_height = ("height in cells", "positional", None, int),
    colors = ("number of colors", "option", "c", int),
    )
def main(root_path, min_width, max_width, min_height, max_height, colors = 4):
    """Encode a grid-coloring problem in CNF."""

    for width in xrange(min_width, max_width + 1):
        for height in xrange(min_height, max_height + 1):
            out_path = os.path.join(root_path, "{0}x{1}.c{2}.cnf".format(width, height, colors))

            with open(out_path, "w") as out_file:
                write_constraints(out_file, colors, width, height)

if __name__ == "__main__":
    plac.call(main)

