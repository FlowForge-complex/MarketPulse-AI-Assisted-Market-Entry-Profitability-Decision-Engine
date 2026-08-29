"""Unit tests for financial logic and break-even calculations."""


def test_revenue_logic():
    """Validates basic revenue multiplication logic."""
    orders = 100
    aov = 500
    revenue = orders * aov
    assert revenue == 50000, "Revenue must equal orders * AOV"


def test_profitability_logic():
    """Validates negative profit when costs exceed revenue."""
    revenue = 50000
    costs = 60000
    profit = revenue - costs
    assert profit < 0, "If costs exceed revenue, profitability should be negative"
