import os.path
import numpy
import plac

@plac.annotations(
    out_path = ("path to output file"),
    runs_path = ("path to runs file"),
    width = ("grid width", "positional", None, int),
    height = ("grid height", "positional", None, int),
    colors = ("number of colors", "option", "c", int),
    )
def main(out_path, cnf_path, width, height, colors = 4):
    """Visualize a grid coloring."""

    # read the initial CNF
    import color_cnf

    (N, raw_clauses) = gridc.encodings.DirectEncoding().encode(4, 22, 17)

if __name__ == "__main__":
    plac.call(main)

