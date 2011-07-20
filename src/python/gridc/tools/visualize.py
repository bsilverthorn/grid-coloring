import csv
import zlib
import base64
import cPickle as pickle
import plac
import numpy
import gridc

def visualize(encoding_name, width, height, answer):
    """Verify and print the coloring."""

    # decode the certificate
    grid = gridc.Grid(width, height)
    encoder = gridc.encoding(encoding_name)(grid)
    coloring = encoder.decode(answer)

    if not numpy.all(coloring < 4) or not numpy.all(coloring >= 0):
        raise ValueError("invalid color in coloring")
    if not grid.is_coloring(coloring):
        raise ValueError("constraint violation in coloring")

    print coloring

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

        for (i, (_, _, _, _, answer_text)) in enumerate(reader):
            if i > 0:
                print

            print "Coloring obtained by run {0}:".format(i)

            if answer_text == "":
                print "(!) None"
            else:
                answer = pickle.loads(zlib.decompress(base64.b64decode(answer_text)))

                visualize(encoding, width, height, answer)

if __name__ == "__main__":
    plac.call(main)

