"""@author: Bryan Silverthorn"""

import numpy
import borg
import gridc

@gridc.named_encoding
class DirectEncoding(gridc.Encoding):
    """The standard direct encoding (de Kleer, 1989)."""

    name = "direct"

    def encode(self):
        """Return a CNF."""

        clauses = []

        clauses.extend(self._clauses_at_least_one())
        clauses.extend(self._clauses_at_most_one())
        clauses.extend(self._clauses_conflict())

        return borg.domains.sat.instance.SAT_Instance.from_clauses(clauses, self.N)

    def decode(self, answer):
        """Return a coloring given a solution to the CNF."""

        coloring = numpy.ones((self.grid.width, self.grid.height), int) * -1

        for x in xrange(self.grid.width):
            for y in xrange(self.grid.height):
                for c in xrange(4):
                    v = self._v(c, x, y)

                    if answer[v - 1] > 0:
                        coloring[x, y] = c

        return coloring

    @property
    def N(self):
        """The number of CNF variables."""

        return self.grid.width * self.grid.height * 4

    def _v(self, c, x, y):
        return 1 + y * self.grid.width * 4 + x * 4 + c

    def _clauses_at_least_one(self):
        """Yield at-least-one constraints."""

        for x in xrange(self.grid.width):
            for y in xrange(self.grid.height):
                yield [self._v(c, x, y) for c in xrange(4)]

    def _clauses_at_most_one(self):
        """Yield at-most-one constraints."""

        for x in xrange(self.grid.width):
            for y in xrange(self.grid.height):
                for c in xrange(4):
                    for d in xrange(c + 1, 4):
                        yield [-self._v(c, x, y), -self._v(d, x, y)]

    def _clauses_conflict(self):
        """Yield conflict constraints."""

        for x0 in xrange(self.grid.width):
            for y0 in xrange(self.grid.height):
                for x1 in xrange(x0 + 1, self.grid.width):
                    for y1 in xrange(y0 + 1, self.grid.height):
                        for c in xrange(4):
                            yield [
                                -self._v(c, x0, y0),
                                -self._v(c, x0, y1),
                                -self._v(c, x1, y0),
                                -self._v(c, x1, y1),
                                ]

@gridc.named_encoding
class IdirectEncoding(DirectEncoding):
    """The idirect encoding (Prestwich, 2004)."""

    name = "idirect"

    def encode(self):
        """Return a CNF."""

        # XXX
        raise NotImplementedError()

@gridc.named_encoding
class SupportEncoding(DirectEncoding):
    """The support encoding (Gent, 2002)."""

    name = "support"

    def encode(self):
        """Return a CNF."""

        clauses = []

        clauses.extend(self._clauses_at_least_one())
        clauses.extend(self._clauses_at_most_one())
        clauses.extend(self._clauses_support())

        return borg.domains.sat.instance.SAT_Instance.from_clauses(clauses, self.N)

    def _clauses_support(self):
        """Yield support constraints."""

        for x0 in xrange(self.grid.width):
            for y0 in xrange(self.grid.height):
                for x1 in xrange(x0 + 1, self.grid.width):
                    for y1 in xrange(y0 + 1, self.grid.height):
                        for clause in self._clauses_support_for(x0, y0, x1, y1):
                            yield clause

    def _clauses_support_for(self, x0, y0, x1, y1):
        """Yield support constraints for one rectangle."""

        corners = [(x0, y0), (x0, y1), (x1, y0), (x1, y1)]

        for (xc, yc) in corners:
            others = [(x, y) for (x, y) in corners if x != xc and y != yc]

            for c in xrange(4):
                support = [self._v(d, xc, yc) for d in xrange(4) if c != d]

                support.extend([-self._v(c, x, y) for (x, y) in corners])

                yield support

@gridc.named_encoding
class MuldirectEncoding(DirectEncoding):
    """The multivalued direct encoding (Selman et al., 1992)."""

    name = "muldirect"

    def encode(self):
        """Return a CNF."""

        clauses = []

        clauses.extend(self._clauses_at_least_one())
        clauses.extend(self._clauses_conflict())

        return borg.domains.sat.instance.SAT_Instance.from_clauses(clauses, self.N)

