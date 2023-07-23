""" Supply and demand curves.

```
| P (Price) axis
|
| *                 @   Supply curve 
|    *           @
|       *     @
|          X <------   Equilibrium point
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
from matplotlib.axes import Axes  # type: ignore


def make_qp_curve(intercept: float, slope: float) -> "Curve":
    """Create curve in Q(P) form."""
    return Curve(1 / slope, -intercept / slope)


@dataclass
class Curve:
    """Create P(Q) line from intercept at vertical axis P and line slope.

    Line equation is `P(Q)  = intercept + slope * Q`.
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
        return -(self.intercept / self.slope) + (p / self.slope)

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

    def plot(self, ax=None, color="black", linewidth=2, max_q=None) -> Axes:
        if ax is None:
            ax = plt.gca()
        p1 = Point(price=self.intercept, quantity=0)
        if max_q:
            p2 = Point(price=self.price(max_q), quantity=max_q)
        else:
            p2 = Point(price=0, quantity=self.q_intercept)
        plotline(ax, p1, p2, color=color, linewidth=linewidth)
        return ax

    def equilibrium_plot(self, other_curve, ax=None, linewidth=2) -> Axes:
        """Plot the intersection of two curves.
        This can't handle taxes or other interventions."""
        if ax is None:
            # not used
            # fig = plt.gcf()
            ax = plt.gca()
        ax.set_ylabel("Price")
        ax.set_xlabel("Quantity")
        curves = self, other_curve
        max_q = max(curve.q_intercept for curve in curves)
        for curve in curves:
            curve.plot(ax=ax, max_q=max_q, linewidth=linewidth)
        e = self.equilibrium(other_curve)
        e.plot_marker(ax, draw_lines=True, annotate=False)
        return ax


def plotline(ax, p1: "Point", p2: "Point", color="black", linewidth=2) -> None:
    """Plot a line connecting two points: *p1* and *p2*."""
    y1, x1 = p1.tuple()
    y2, x2 = p2.tuple()
    ax.plot([x1, x2], [y1, y2], color=color, linewidth=linewidth)


def clean_axis(ax: Axes) -> None:
    """Сode for cleaning axis with unclear behaviour."""
    ax.spines["left"].set_position("zero")
    ax.spines["bottom"].set_position("zero")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


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
    def consumer_surplus(self, price: float) -> float:
        """Calculate consumer surplus at given *price*."""
        tri_height = self.intercept - price
        tri_base = self.q(price)
        return 0.5 * tri_base * tri_height

    def plot_surplus(self, price, ax=None):
        """Fill consumer surplus (CS) area."""
        if ax == None:
            ax = plt.gca()
        ax.fill_between(
            x=[0, self.q(price)], y1=[self.intercept, price], y2=price, alpha=0.1
        )


class Supply(Curve):
    def producer_surplus(self, price: float) -> float:
        """Calculate producer surplus (PS) at a given *price*."""
        raise NotImplementedError

    def plot_surplus(self, price, ax=None):
        """Fill producer surplus (PS) area."""
        if ax == None:
            ax = plt.gca()
        ax.fill_between(
            x=[0, self.q(price)],
            y1=[self.intercept, price],
            y2=price,
            color="C1",
            alpha=0.1,
        )
