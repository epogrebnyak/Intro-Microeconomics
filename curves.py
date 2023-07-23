""" Supply and demand curves.

| P
|
| *                 @   Supply curve 
|    *           @
|       *     @
|          X <------   Intercept
|      @      *
|   @            *  
|@                  *   Demand curve 
_______________________*____________ Q 
                       ^ q_intercept
"""
from dataclasses import dataclass
from typing import Tuple

import numpy as np


def make_qp_curve(intercept: float, slope: float) -> "Curve":
    """Create curve in Q(P) form."""
    return Curve(1 / slope, -intercept / slope)


@dataclass
class Curve:
    """Create P(Q) form curve with intercept and slope.
    This is an inverse=True curve in econ101.py.
    """

    slope: float
    intercept: float

    @property
    def q_intercept(self):
        """Curve intercept at quantity axis."""
        return -intercept / slope if slope else np.nan

    def q(self, p):
        """Quantity demanded or supplied at price p."""
        return (self.intercept / (-self.slope)) + (p / self.slope)

    def p(self, q):
        """Price when quantity demanded/supplied is at q."""
        return self.intercept + self.slope * q

    def vertical_shift(self, delta: float) -> "Curve":
        """Shift curve vertically by amount delta. Shifts demand curve to the right.
        Shifts supply curve to the left."""
        self.intercept += delta
        return self

    def horizontal_shift(self, delta: float) -> "Curve":
        """Shift curve horizontally by amount delta. Positive values are shifts to the right."""
        return vertical_shift(delta * -self.slope)

    def equilibrium(self, other_curve: "Curve") -> Tuple[float, float]:
        """Returns a tuple (p, q). Allows for negative prices or quantities."""

        v1 = np.array([1, -self.slope])
        v2 = np.array([1, -other_curve.slope])

        b = self.intercept, other_curve.intercept

        A = np.matrix((v1, v2))
        b = np.matrix(b).T

        x = np.linalg.inv(A) * b
        x = x.squeeze()

        return Point(p=x[0, 0], q=x[0, 1])


@dataclass
class Point:
    p: float
    q: float

    def round(self, precision) -> "Point":
        return Point(round(self.p, precision), round(self.q, precision))


class Demand(Curve):
    pass


class Supply(Curve):
    pass
