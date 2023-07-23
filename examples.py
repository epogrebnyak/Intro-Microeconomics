# FIXME: does not work

from curves import Demand, Supply
import matplotlib.pyplot as plt

demand = Demand(intercept=12, slope=-2)
supply = Supply(intercept=0, slope=1)
ax = demand.plot(max_q=demand.q_intercept)
plt.savefig("demand.png")
supply.plot(ax=ax, max_q=6)
plt.savefig("demand_supply.png")

demand.equilibrium_plot(s)
demand.horizontal_shift(2)
demand.equilibrium_plot(s)
