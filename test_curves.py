from curves import Demand, Supply


def test_equilibrium():
    demand = Demand(intercept=12, slope=-2)
    supply = Supply(intercept=0, slope=1)
    x = demand.equilibrium(supply).round(4)
    assert x.p == 4
    assert demand.p(x.q) == 4
    assert supply.p(x.q) == 4
