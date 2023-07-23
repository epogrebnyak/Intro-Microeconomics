""" Supply and demand curves.

```
| P (Price) axis
|
| *                 @   Supply curve 
|    *           @
|       *     @
|          X <------   Intercept
|      @      *
|   @            *  
|@                  *   Demand curve 
_______________________*____________ Q (Quantity) axis 
                       ^ q_intercept
```
"""
from dataclasses import dataclass

import numpy as np
import matplotlib.pyplot as plt  # type: ignore


def make_qp_curve(intercept: float, slope: float) -> "Curve":
    """Create curve in Q(P) form."""
    return Curve(1 / slope, -intercept / slope)


@dataclass
class Curve:
    """Create P(Q) line from intercept at vertical axis P and line slope.

    Line equation is `P = intercept + slope * Q`.
    """

    intercept: float
    slope: float

    @property
    def q_intercept(self):
        """Line intercept at quantity axis."""
        return -self.intercept / self.slope if self.slope else np.nan

    def quantity(self, price):
        """Quantity demanded or supplied at a given *price*."""
        return self.q(price)

    def q(self, p):
        """Shorthand for quantity() method."""
        return (self.intercept / (-self.slope)) + (p / self.slope)

    def price(self, quantity):
        """Price given *quantity* demanded or supplied."""
        return self.p(quantity)

    def p(self, q):
        """Shorthand for price() method."""
        return self.intercept + self.slope * q

    def vertical_shift(self, delta: float) -> "Curve":
        """Shift curve vertically by amount delta. Shifts demand curve to the right.
        Shifts supply curve to the left."""
        self.intercept += delta
        return self

    def horizontal_shift(self, delta: float) -> "Curve":
        """Shift curve horizontally by amount delta.
        Positive values are shifts to the right."""
        return self.vertical_shift(delta * -self.slope)

    def equilibrium(self, other_curve: "Curve") -> "Point":
        """Returns a point of intersection of two curves. 
        Allows for negative prices or quantities."""
        v1 = np.array([1, -self.slope])
        v2 = np.array([1, -other_curve.slope])
        A = np.array([v1, v2])
        # FIXME: must use ndarray of matrix
        b = self.intercept, other_curve.intercept
        b = np.matrix(b).T  # type: ignore
        x = np.linalg.inv(A) * b
        x = x.squeeze()
        return Point(price=x[0, 0], quantity=x[0, 1])

    def plot(self, ax=None, color="black", linewidth=2, max_q=None, clean=False):
        if ax is None:
            ax = plt.gca()

        # core plot
        q_ = self.q_intercept
        if np.isnan(q_):  # if slope is 0,
            q_ = 10**10  # we set the intercept very far away
        x2 = np.max([q_, max_q])
        y2 = self.intercept + self.slope * x2

        xs = np.linspace(0, x2, 2)
        ys = np.linspace(self.intercept, y2, 2)

        ax.plot(xs, ys, color=color, linewidth=linewidth)

        if clean:
            ax.spines["left"].set_position("zero")
            ax.spines["bottom"].set_position("zero")
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
        return ax

    def equilibrium_plot(
        self, other_curve, ax=None, linewidth=2, annotate=False, clean=True
    ):
        """Plot the intersection of two curves.
        This can't handle taxes or other interventions."""
        if ax is None:
            fig, ax = plt.gcf(), plt.gca()
        ax.set_ylabel("Price")
        ax.set_xlabel("Quantity")
        for curve in self, other_curve:
            curve.plot(ax=ax, linewidth=linewidth)
        e = self.equilibrium(other_curve)
        e.plot_marker(ax, draw_lines=True, annotate=annotate)

@dataclass
class Point:
    price: float
    quantity: float

    def round(self, precision) -> "Point":
        """Round point coordinates to *precision* digits.
        Useful when working with values like 0.999999."""
        p, q = round(self.price, precision), round(self.quantity, precision)
        return Point(p, q)

    def tuple(self):
        """Get point coordinates as a tuple."""
        return self.price, self.quantity

    def plot_marker(self, ax, draw_lines=True, annotate=True):
        """Draw a point with optional dashed lines and annotation."""
        p, q = self.tuple()

        # draw marker
        ax.plot([q], [p], marker="o")

        # dashed lines around market price and quantity
        if draw_lines:
            ax.plot([0, q], [p, p], linestyle="dashed", color="C0")
            ax.plot([q, q], [0, p], linestyle="dashed", color="C0")

        # annotation on the plot
        if annotate:
            s = " $p = {:.1f}, q = {:.1f}$".format(p, q)
            ax.text(q, p, s, ha="left", va="center")


class Demand(Curve):
    pass


class Supply(Curve):
    pass
