CREATE TABLE IF NOT EXISTS users (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

INSERT INTO users (name, email)
SELECT 'Benchmark User ' || g, 'user' || g || '@example.com'
FROM generate_series(1, 10000) AS g
ON CONFLICT (email) DO NOTHING;

ANALYZE users;
