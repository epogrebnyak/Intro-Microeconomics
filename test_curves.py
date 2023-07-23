from curves import Demand, Supply


def test_q_intercept():
    assert Demand(intercept=12, slope=-2).q_intercept == 6


def test_shifts():
    assert Demand(20, -2) == Demand(12, -2).vertical_shift(2).horizontal_shift(3)


def test_equilibrium():
    demand = Demand(intercept=12, slope=-2)
    supply = Supply(intercept=0, slope=1)
    x = demand.equilibrium(supply).round(4)
    assert x.price == 4
    assert demand.price(x.quantity) == 4
    assert supply.price(x.quantity) == 4


def test_plotting():
    from curves import Demand, Supply, clean_axis

    demand = Demand(intercept=12, slope=-2)
    demand.plot()
    supply = Supply(intercept=0, slope=1)
    supply.plot()
    ax = demand.equilibrium_plot(supply)
    demand.horizontal_shift(2)
    demand.equilibrium_plot(supply, ax=ax)
    e = demand.equilibrium(supply).round(2)
    e.plot_marker(ax, annotate=True)
    demand.plot_surplus(e.price, ax=ax)
    supply.plot_surplus(e.price, ax=ax)
    clean_axis(ax)
