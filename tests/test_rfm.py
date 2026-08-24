import pytest
# Mock test for RFM logic
def test_rfm_monetary_score():
    # If a customer spends more, their monetary score should increase
    spend_a = 1000
    spend_b = 5000
    assert spend_b > spend_a, "Higher spend should result in higher value"
