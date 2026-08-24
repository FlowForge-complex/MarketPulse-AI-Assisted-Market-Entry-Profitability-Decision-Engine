-- Q5: What is monthly customer retention?
WITH FirstOrder AS (
    SELECT customer_id, MIN(DATE_TRUNC('month', order_date)) as cohort_month
    FROM orders
    GROUP BY customer_id
),
OrderMonths AS (
    SELECT DISTINCT customer_id, DATE_TRUNC('month', order_date) as order_month
    FROM orders
)
SELECT 
    fo.cohort_month,
    EXTRACT(MONTH FROM AGE(om.order_month, fo.cohort_month)) as months_since_first_order,
    COUNT(DISTINCT om.customer_id) as active_customers
FROM FirstOrder fo
JOIN OrderMonths om ON fo.customer_id = om.customer_id
GROUP BY fo.cohort_month, months_since_first_order
ORDER BY fo.cohort_month, months_since_first_order;
