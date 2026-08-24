-- Q1: Which city generates the highest revenue?
SELECT 
    c.city_name,
    COUNT(DISTINCT o.order_id) as total_orders,
    SUM(oi.quantity * oi.unit_price) as gross_revenue
FROM cities c
JOIN orders o ON c.city_id = o.city_id
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY c.city_name
ORDER BY gross_revenue DESC;
