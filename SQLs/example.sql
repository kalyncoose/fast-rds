-- Create new table for example database
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE TABLE IF NOT EXISTS example (
	id uuid DEFAULT uuid_generate_v4(),
	email VARCHAR(50) UNIQUE NOT NULL,
	name VARCHAR(50) NOT NULL,
	created_at TIMESTAMPTZ NOT NULL DEFAULT Now(),
	updated_at TIMESTAMPTZ NOT NULL DEFAULT Now(),
	active BOOLEAN NOT NULL DEFAULT 't',
	PRIMARY KEY (id)
);
COMMENT ON COLUMN example.email IS 'personal_data';
COMMENT ON COLUMN example.name IS 'personal_data';
COMMENT ON TABLE example IS 'This table contains sensitive user information.';
