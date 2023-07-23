from econ101 import Demand, Supply


def test_equilibrium():
    demand = Demand(12, -2)
    supply = Supply(0, 1)
    eq = d.equilibrium(s).round(4)
    assert eq.p == 1
    assert demand.p(e.q) == 1
    assert supply.p(e.q) == 1
