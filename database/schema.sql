-- MarketPulse Database Schema

CREATE TABLE cities (
    city_id SERIAL PRIMARY KEY,
    city_name VARCHAR(50),
    state VARCHAR(50),
    population INT,
    households INT,
    population_density INT,
    urbanization DECIMAL(5,2),
    mpce INT,
    internet_penetration DECIMAL(5,2),
    economic_growth DECIMAL(5,2),
    income_proxy INT,
    ecommerce_adoption DECIMAL(5,2)
);

CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    city_id INT REFERENCES cities(city_id),
    signup_date DATE,
    age_group VARCHAR(20),
    customer_segment VARCHAR(50)
);

CREATE TABLE products (
    product_id INT PRIMARY KEY,
    category VARCHAR(50),
    subcategory VARCHAR(50),
    product_name VARCHAR(100),
    unit_cost INT,
    selling_price INT
);

CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id),
    city_id INT REFERENCES cities(city_id),
    order_date DATE,
    order_status VARCHAR(20),
    delivery_time INT,
    discount INT,
    delivery_fee INT
);

CREATE TABLE order_items (
    order_id INT REFERENCES orders(order_id),
    product_id INT REFERENCES products(product_id),
    quantity INT,
    unit_price INT,
    cost INT
);

CREATE TABLE competitors (
    competitor_id SERIAL PRIMARY KEY,
    competitor_name VARCHAR(100)
);

CREATE TABLE competitor_pricing (
    competitor_id INT REFERENCES competitors(competitor_id),
    city_id INT REFERENCES cities(city_id),
    product_category VARCHAR(50),
    listed_price INT,
    discount INT,
    observed_price INT,
    observation_date DATE
);

CREATE TABLE operating_costs (
    city_id INT REFERENCES cities(city_id),
    rent INT,
    labor_cost INT,
    delivery_cost INT,
    utilities INT,
    other_fixed_cost INT
);

CREATE TABLE marketing_spend (
    city_id INT REFERENCES cities(city_id),
    month DATE,
    spend INT,
    new_customers INT
);

CREATE TABLE city_metrics (
    city_id INT REFERENCES cities(city_id),
    market_size BIGINT,
    growth_rate DECIMAL(5,2),
    competition_score INT,
    demand_score INT,
    income_score INT,
    cost_score INT
);
