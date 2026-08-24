def estimate_tam(population, hh_size, internet_pen, adoption_rate, aov, orders_pm):
    households = population / hh_size
    addressable_hh = households * internet_pen
    target_hh = addressable_hh * adoption_rate
    annual_market_size = target_hh * orders_pm * aov * 12
    return annual_market_size

if __name__ == "__main__":
    tam = estimate_tam(
        population=12500000, hh_size=4, internet_pen=0.75, 
        adoption_rate=0.22, aov=450, orders_pm=2
    )
    print(f"Estimated Bangalore TAM: ₹{tam/10**9:.2f} Billion")
