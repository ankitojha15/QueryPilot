-- Small sample data for learning and eval.

CREATE TABLE IF NOT EXISTS customers (
  id SERIAL PRIMARY KEY,
  org_id INT NOT NULL,
  name TEXT NOT NULL,
  email TEXT NOT NULL,
  city TEXT NOT NULL,
  state TEXT NOT NULL,
  created_at DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS products (
  id SERIAL PRIMARY KEY,
  org_id INT NOT NULL,
  name TEXT NOT NULL,
  price INT NOT NULL
);

CREATE TABLE IF NOT EXISTS orders (
  id SERIAL PRIMARY KEY,
  org_id INT NOT NULL,
  customer_id INT NOT NULL,
  product_id INT NOT NULL,
  amount INT NOT NULL,
  status TEXT NOT NULL,
  created_at DATE NOT NULL
);

INSERT INTO customers (org_id, name, email, city, state, created_at) VALUES
(1, 'Amit', 'amit@test.com', 'Delhi', 'Delhi', '2024-01-05'),
(1, 'Neha', 'neha@test.com', 'Mumbai', 'Maharashtra', '2024-02-10'),
(2, 'Ravi', 'ravi@test.com', 'Delhi', 'Delhi', '2024-03-12');

INSERT INTO products (org_id, name, price) VALUES
(1, 'Shoes', 2000),
(1, 'Bag', 1500);

INSERT INTO orders (org_id, customer_id, product_id, amount, status, created_at) VALUES
(1, 1, 1, 2000, 'paid', '2024-04-01'),
(1, 2, 2, 1500, 'paid', '2024-04-05'),
(1, 1, 2, 1500, 'refund', '2024-04-07');
