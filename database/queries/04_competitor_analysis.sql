-- Analyze competitor pricing across cities
SELECT 
    city_id,
    product_category,
    AVG(observed_price) as avg_market_price,
    MAX(discount) as max_market_discount
FROM competitor_pricing
GROUP BY city_id, product_category
ORDER BY city_id;
