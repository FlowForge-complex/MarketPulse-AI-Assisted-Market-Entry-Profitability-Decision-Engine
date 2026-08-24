-- Q3 & Q4: Which customer segment generates the most revenue and highest contribution margin?
WITH SegmentData AS (
    SELECT 
        cu.customer_segment,
        SUM(oi.quantity * oi.unit_price) as revenue,
        SUM(oi.quantity * oi.cost) as cogs,
        SUM(o.discount) as total_discounts
    FROM customers cu
    JOIN orders o ON cu.customer_id = o.customer_id
    JOIN order_items oi ON o.order_id = oi.order_id
    GROUP BY cu.customer_segment
)
SELECT 
    customer_segment,
    revenue,
    revenue - cogs - total_discounts as contribution_margin,
    ROUND((revenue - cogs - total_discounts) * 100.0 / revenue, 2) as margin_percentage
FROM SegmentData
ORDER BY contribution_margin DESC;
