-- Q9: Which city has the highest expected contribution after considering demand, competition, and operating costs?
WITH CityRevenue AS (
    SELECT 
        o.city_id,
        SUM(oi.quantity * oi.unit_price) as gross_revenue,
        SUM(oi.quantity * oi.cost) as cogs,
        SUM(o.delivery_fee) as delivery_revenue
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    GROUP BY o.city_id
)
SELECT 
    c.city_name,
    cr.gross_revenue,
    (cr.gross_revenue - cr.cogs + cr.delivery_revenue) as contribution
FROM cities c
JOIN CityRevenue cr ON c.city_id = cr.city_id
ORDER BY contribution DESC;
