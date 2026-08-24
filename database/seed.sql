-- Seed Script for MarketPulse
-- Assuming PostgreSQL `COPY` command.
-- Ensure to replace absolute paths if running locally in a different environment.

-- 1. Cities (Manual insert for consistency with synthetic IDs 1-5)
INSERT INTO cities (city_id, city_name, state, population, households, population_density, urbanization, mpce, internet_penetration, economic_growth, income_proxy, ecommerce_adoption) VALUES
(1, 'Bengaluru', 'Karnataka', 12500000, 3125000, 4381, 100, 6500, 75, 8.5, 850000, 22),
(2, 'Mumbai', 'Maharashtra', 20500000, 4500000, 21000, 100, 7200, 72, 7.8, 900000, 20),
(3, 'Delhi NCR', 'Delhi', 28000000, 6000000, 11320, 98, 6800, 78, 8.0, 880000, 25),
(4, 'Hyderabad', 'Telangana', 10000000, 2400000, 10477, 100, 6100, 68, 8.2, 750000, 18),
(5, 'Pune', 'Maharashtra', 7000000, 1600000, 6500, 100, 5900, 70, 7.5, 720000, 16);

-- For synthetic data, use COPY (or \copy in psql)
-- \copy customers FROM '../data/synthetic/customers.csv' DELIMITER ',' CSV HEADER;
-- \copy products FROM '../data/synthetic/products.csv' DELIMITER ',' CSV HEADER;
-- \copy orders FROM '../data/synthetic/orders.csv' DELIMITER ',' CSV HEADER;
-- \copy order_items FROM '../data/synthetic/order_items.csv' DELIMITER ',' CSV HEADER;
