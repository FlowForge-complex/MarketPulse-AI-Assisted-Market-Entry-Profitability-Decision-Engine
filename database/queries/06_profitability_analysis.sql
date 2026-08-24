-- Q7 & Q8: Profitability after adjusting for delivery costs and product margins
SELECT 
    p.category,
    SUM(oi.quantity * oi.unit_price) as category_revenue,
    SUM(oi.quantity * oi.cost) as category_cost,
    SUM(oi.quantity * oi.unit_price) - SUM(oi.quantity * oi.cost) as gross_profit
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY p.category
ORDER BY gross_profit DESC;
