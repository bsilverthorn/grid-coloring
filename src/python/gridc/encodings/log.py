"""@author: Bryan Silverthorn <bcs@cargo-cult.org>"""

import numpy
import borg
import gridc

@gridc.named_encoding
class LogEncoding(gridc.Encoding):
    name = "log"

    def encode(self):
        def p(b):
            return 1 if b else -1

        def rclause(x0, y0, x1, y1, b0, b1):
            return [
                p(b0) * self._v(x0, y0, 0),
                p(b1) * self._v(x0, y0, 1),
                p(b0) * self._v(x0, y1, 0),
                p(b1) * self._v(x0, y1, 1),
                p(b0) * self._v(x1, y0, 0),
                p(b1) * self._v(x1, y0, 1),
                p(b0) * self._v(x1, y1, 0),
                p(b1) * self._v(x1, y1, 1),
                ]

        clauses = []

        for x0 in xrange(self.grid.width):
            for y0 in xrange(self.grid.height):
                for x1 in xrange(x0 + 1, self.grid.width):
                    for y1 in xrange(y0 + 1, self.grid.height):
                        clauses.append(rclause(x0, y0, x1, y1, True, True))
                        clauses.append(rclause(x0, y0, x1, y1, True, False))
                        clauses.append(rclause(x0, y0, x1, y1, False, True))
                        clauses.append(rclause(x0, y0, x1, y1, False, False))

        return borg.domains.sat.instance.SAT_Instance.from_clauses(clauses, self.N)

    def decode(self, answer):
        """Return a coloring given a solution to the CNF."""

        coloring = numpy.ones((self.grid.width, self.grid.height), int) * -1

        for x in xrange(self.grid.width):
            for y in xrange(self.grid.height):
                p0 = 1 if answer[self._v(x, y, 0) - 1] > 0 else 0
                p1 = 1 if answer[self._v(x, y, 1) - 1] > 0 else 0

                coloring[x, y] = p0 + 2 * p1

        return coloring

    @property
    def N(self):
        return self.grid.width * self.grid.height * 2

    def _v(self, x, y, b):
        return 1 + y * self.grid.width * 2 + x * 2 + b

