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
import matplotlib.pyplot as plt


def make_qp_curve(intercept: float, slope: float) -> "Curve":
    """Create curve in Q(P) form."""
    return Curve(1 / slope, -intercept / slope)


@dataclass
class Curve:
    """Create P(Q) form curve with intercept and slope.
    This is an inverse=True curve in econ101.py.
    """

    intercept: float
    slope: float

    @property
    def q_intercept(self):
        """Curve intercept at quantity axis."""
        return -self.intercept / self.slope if self.slope else np.nan

    def quantity(self, price):
        """Quantity demanded or supplied at *price*."""
        return self.q(price)

    def q(self, p):
        return (self.intercept / (-self.slope)) + (p / self.slope)

    def price(self, quantity):
        """Price when quantity demanded/supplied is at q."""
        return self.p(quantity)

    def p(self, q):
        return self.intercept + self.slope * q

    def vertical_shift(self, delta: float) -> "Curve":
        """Shift curve vertically by amount delta. Shifts demand curve to the right.
        Shifts supply curve to the left."""
        self.intercept += delta
        return self

    def horizontal_shift(self, delta: float) -> "Curve":
        """Shift curve horizontally by amount delta. Positive values are shifts to the right."""
        return self.vertical_shift(delta * -self.slope)

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

    def plot(self, ax=None, color="black", linewidth=2, max_q=10, clean=False):
        if ax is None:
            ax = plt.gca()

        # core plot
        q_ = self.q_intercept
        if np.isnan(q_):  # if slope is 0
            q_ = 10**10
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
        """Plot the intersection of two curves. This can't handle taxes or other interventions."""
        if ax == None:
            fig, ax = plt.gcf(), plt.gca()

        for curve in self, other_curve:
            curve.plot(ax=ax, linewidth=linewidth)

        ax.set_ylabel("Price")
        ax.set_xlabel("Quantity")

        # dashed lines around market price and quantity
        p, q = self.equilibrium(other_curve).tuple()
        ax.plot([0, q], [p, p], linestyle="dashed", color="C0")
        ax.plot([q, q], [0, p], linestyle="dashed", color="C0")
        ax.plot([q], [p], marker="o")

        # annotation on the plot
        if annotate:
            s = " $p = {:.1f}, q = {:.1f}$".format(p, q)
            ax.text(q, p, s, ha="left", va="center")


@dataclass
class Point:
    price: float
    quantity: float

    def round(self, precision) -> "Point":
        p, q = round(self.price, precision), round(self.quantity, precision)
        return Point(p, q)

    def tuple(self):
        return self.price, self.quantity

    def plot_marker_with_dashed_lines(self, ax):  
        p, q = self.tuple()
        ax.plot([0, q], [p, p], linestyle="dashed", color="C0")
        ax.plot([q, q], [0, p], linestyle="dashed", color="C0")
        ax.plot([q], [p], marker="o")


class Demand(Curve):
    pass


class Supply(Curve):
    pass

