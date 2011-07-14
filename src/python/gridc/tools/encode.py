import os.path
import plac
import gridc

@plac.annotations(
    root_path = ("path to output directory"),
    encoding_name = ("name of encoding"),
    min_width = ("min width in cells", "positional", None, int),
    max_width = ("max width in cells", "positional", None, int),
    min_height = ("height in cells", "positional", None, int),
    max_height = ("height in cells", "positional", None, int),
    )
def main(root_path, encoding_name, min_width, max_width, min_height, max_height):
    """Encode a grid-coloring problem in CNF."""

    for width in xrange(min_width, max_width + 1):
        for height in xrange(min_height, max_height + 1):
            # encode the instance
            grid = gridc.encodings.Grid(width, height)
            encoding = gridc.encodings.by_name[encoding_name]
            instance = encoding.encode(grid)

            # write it to disk
            out_name = "{0}x{1}.{2}.cnf".format(width, height, encoding_name)
            out_path = os.path.join(root_path, out_name)

            with open(out_path, "w") as out_file:
                instance.write(out_file)

if __name__ == "__main__":
    plac.call(main)

