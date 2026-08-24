import pytest

def test_market_sizing():
    # TAM should increase if adoption rate increases
    def calculate_tam(adoption_rate):
        return 1000000 * adoption_rate * 500 * 12
    
    tam_low = calculate_tam(0.10)
    tam_high = calculate_tam(0.20)
    assert tam_high > tam_low, "TAM must scale linearly with adoption rate"
