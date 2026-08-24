import pytest

def test_weights_sum_to_100():
    wA = {"Market": 0.25, "Growth": 0.30, "Demand": 0.20, "Competition": 0.10, "Cost": 0.10, "Income": 0.05}
    assert sum(wA.values()) == 1.0, "Scenario A weights must sum to 1.0"
    
    wB = {"Market": 0.20, "Growth": 0.10, "Demand": 0.15, "Competition": 0.20, "Cost": 0.25, "Income": 0.10}
    assert sum(wB.values()) == 1.0, "Scenario B weights must sum to 1.0"
