"""Draw three curves, markers and surpluses."""

from curves import Demand, Supply, clean_axis
import matplotlib.pyplot as plt

# Initial curves
demand = Demand(intercept=12, slope=-2)
demand.plot()
supply = Supply(intercept=0, slope=1)
supply.plot()
ax = demand.equilibrium_plot(supply)

# Shift demand
demand.horizontal_shift(2)
demand.vertical_shift(-1)
demand.equilibrium_plot(supply, ax=ax)
e = demand.equilibrium(supply).round(2)
e.plot_marker(ax, annotate=True)
print(e)

# Plot consumer surplus (CS) and producer surplus (PS)
demand.plot_surplus(e.price, ax=ax)
supply.plot_surplus(e.price, ax=ax)

# Clean and save
clean_axis(ax)
plt.savefig("demand_supply.png")
