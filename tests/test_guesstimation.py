"""Unit tests for bottom-up Total Addressable Market (TAM) guesstimation."""

from src.core.types import TAMParameters
from src.guesstimation.market_sizing import (
    calculate_tam,
    get_default_bengaluru_tam,
)


def test_tam_calculation_math():
    """Validates mathematical correctness of TAM derivation."""
    params = TAMParameters(
        target_city="Bengaluru",
        population=10000000,
        household_size=4.0,
        internet_penetration_rate=0.80,
        ecommerce_adoption_rate=0.25,
        target_category_share=0.40,
        orders_per_month_per_hh=2.0,
        average_order_value=500.0,
    )
    res = calculate_tam(params, benchmark_tam_crores=240.0)
    assert res.total_households == 2500000
    assert res.connected_households == 2000000
    assert res.active_ecommerce_households == 500000
    assert res.target_customers == 200000
    assert res.annual_order_volume == 4800000
    assert res.annual_tam_inr == 2400000000.0
    assert res.annual_tam_inr_crores == 240.0
    assert res.sanity_check_passed is True


def test_default_bengaluru_tam():
    """Validates default Bengaluru market sizing parameters."""
    res = get_default_bengaluru_tam()
    assert res.city == "Bengaluru"
    assert res.annual_tam_inr_crores > 100.0
    assert res.sanity_check_passed is True
