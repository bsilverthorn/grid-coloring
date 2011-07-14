import csv
import zlib
import base64
import cPickle as pickle
import plac
import numpy
import gridc

@plac.annotations(
    runs_path = ("path to runs file"),
    encoding = ("name of the encoding"),
    width = ("grid width", "positional", None, int),
    height = ("grid height", "positional", None, int),
    )
def main(runs_path, encoding, width, height):
    """Visualize a grid coloring."""

    # load the certificate
    with open(runs_path) as runs_file:
        reader = csv.reader(runs_file)

        reader.next()

        (_, _, _, _, answer_text) = reader.next()

    answer = pickle.loads(zlib.decompress(base64.b64decode(answer_text)))

    # decode the certificate
    grid = gridc.encodings.Grid(width, height)
    encoding = gridc.encodings.by_name[encoding]
    coloring = encoding.decode(grid, answer)

    if not numpy.all(coloring < 4) or not numpy.all(coloring >= 0):
        raise ValueError("invalid color in coloring")
    if not grid.is_coloring(coloring):
        raise ValueError("constraint violation in coloring")

    print coloring

if __name__ == "__main__":
    plac.call(main)

