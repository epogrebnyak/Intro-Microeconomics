#%%
from curves import Demand, Supply
import matplotlib.pyplot as plt

demand = Demand(intercept=12, slope=-2)
supply = Supply(intercept=0, slope=1)
ax = demand.plot(max_q=demand.q_intercept)
supply.plot(ax=ax, max_q=6)
demand.equilibrium_plot(supply, ax=ax)
demand.horizontal_shift(2)
demand.equilibrium_plot(supply, ax=ax)
plt.savefig("_demand_supply.png")

# %%
