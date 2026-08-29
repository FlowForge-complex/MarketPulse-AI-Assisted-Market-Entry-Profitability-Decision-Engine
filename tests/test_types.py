"""Unit tests for typed dataclasses and input validation constraints."""

import pytest

from src.core.types import (
    CityMetrics,
    CustomerRecord,
    ScoringWeights,
    TAMParameters,
    ValidationError,
)


def test_city_metrics_validation():
    """Validates boundary constraints for city metrics."""
    # Valid instance
    city = CityMetrics(
        city_id=1,
        city="Bengaluru",
        state="Karnataka",
        population=12500000,
        households=3125000,
        population_density=4381,
        urbanization=100.0,
        mpce=6500,
        internet_penetration=75.0,
        economic_growth=8.5,
        income_proxy=850000,
        ecommerce_adoption=22.0,
    )
    assert city.city == "Bengaluru"

    # Invalid negative population
    with pytest.raises(ValidationError):
        CityMetrics(
            city_id=1,
            city="Invalid",
            state="State",
            population=-500,
            households=100,
            population_density=100,
            urbanization=50.0,
            mpce=1000,
            internet_penetration=50.0,
            economic_growth=5.0,
            income_proxy=100000,
            ecommerce_adoption=10.0,
        )


def test_customer_record_validation():
    """Validates segment classification values."""
    cust = CustomerRecord(
        customer_id=1,
        city_id=1,
        signup_date="2026-01-01",
        age_group="26-35",
        customer_segment="Frequent",
    )
    assert cust.customer_segment == "Frequent"

    with pytest.raises(ValidationError):
        CustomerRecord(
            customer_id=2,
            city_id=1,
            signup_date="2026-01-01",
            age_group="26-35",
            customer_segment="UnknownSegment",
        )


def test_scoring_weights_validation():
    """Validates that scoring weights must sum to exactly 1.0."""
    valid_w = ScoringWeights(
        economic_growth=0.25,
        competition_inverse=0.25,
        cost_efficiency=0.15,
        demand_index=0.15,
        market_size=0.10,
        income_level=0.10,
    )
    assert round(sum(valid_w.to_dict().values()), 2) == 1.00

    with pytest.raises(ValidationError):
        ScoringWeights(
            economic_growth=0.50,
            competition_inverse=0.50,
            cost_efficiency=0.50,
            demand_index=0.10,
            market_size=0.10,
            income_level=0.10,
        )


def test_tam_parameters_validation():
    """Validates TAM guesstimation parameters."""
    valid_tam = TAMParameters(
        target_city="Bengaluru",
        population=12500000,
        household_size=4.0,
        internet_penetration_rate=0.75,
        ecommerce_adoption_rate=0.22,
        target_category_share=0.35,
        orders_per_month_per_hh=2.0,
        average_order_value=450.0,
    )
    assert valid_tam.target_city == "Bengaluru"

    with pytest.raises(ValidationError):
        TAMParameters(
            target_city="InvalidCity",
            population=1000000,
            household_size=4.0,
            internet_penetration_rate=1.5,  # Rate > 1.0 is invalid
            ecommerce_adoption_rate=0.20,
            target_category_share=0.30,
            orders_per_month_per_hh=1.0,
            average_order_value=100.0,
        )
