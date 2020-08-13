# fast-rds

`[fast-rds]` is a proof-of-concept tool designed to streamline database creation using a configuration file and code generation to create and execute SQL based on a provided schema.

## Demo

### !automate command
 ![!automate command demo](/demos/demo-automate.gif)
 ![Resulting database in RDS](/demos/demo-automate.png)

The `!automate [option]` command will create the database given the config JSON file in the `./configs/` directory. Then, once the database status is `Available`, it will generate an SQL file based on the JSON schema file in the `./schemas/` directory. Once the SQL is generated, it will execute it on the database and then make the database no longer publicly accessible in AWS.

### Database Configuration
When automated, the database instance is configured with the values from a file in the `./configs/` directory.

Example:
```json
{
    "DBName": "test",
    "DBInstanceIdentifier": "my-example-db",
    "AllocatedStorage": 100,
    "DBInstanceClass": "db.t2.micro",
    "Engine": "postgres",
    "MasterUsername": "postgres",
    "MasterUserPassword": "password"
}
```

A full list of RDS configuration parameters is provided in the `./configs/example.json` file.

### JSON Schema to PostgreSQL

After the database is created, the schema provided in `./schemas/` is used to generate a `.sql` file.

Schema:
```json
{
  "table": [
    { "field": "id", "type": "uuid", "primary_key": true },
    { "field": "email", "type": "text", "unique": true, "not_null": true, "personal_data": true },
    { "field": "name", "type": "text", "not_null": true, "personal_data": true },
    { "field": "created_at", "type": "date", "default": "Now()", "not_null": true },
    { "field": "updated_at", "type": "date", "default": "Now()", "not_null": true },
    { "field": "active", "type": "boolean", "not_null": true, "default": true }
  ],
  "description": "This table contains sensitive user information."
}
```
Generates:
```sql
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
```

## Getting Started

### Prerequisites

#### Python 3

This project was created using Python 3.8.5, please [download and install](https://www.python.org/downloads/) the latest Python version.

#### AWS CLI

In order to run fast-rds, you must have the latest AWS CLI version installed and configured.

[You may select and install AWS CLI here.](https://aws.amazon.com/cli/)

To configure your AWS CLI, use `aws configure` once installed.

**Note:** It is recommended that you configure your AWS CLI based on an IAM user's security credentials.

#### Pypi Packages

This project requires the following pypi packages to be installed:
* `pip install boto3` - Use AWS in Python
* `pip install psycopg2` - Connect and Execute Postgresql in Python
* `pip install progress` - Progress/Loading Bar
* `pip install colorama` - Text color support for Windows Command Prompt/Linux Terminals
* `pip install js-regex` - Use JavaScript regex in Python

## Additional Commands
While the `!automate [option]` command is great for when both your configuration file and schema file is ready, you can always use the `!create` command to have a more hand-held experience.

### !create command
#### Using !create with config
![!create command demo with config](/demos/demo-create-with-config.gif)
The `!create` command will initially ask if you want to create with or without a config, type 'y' to create with a config. You will have a chance to confirm your configuration. Upon confirmation, the database will be created. Once the database status is `Available`, you will be prompted to enter the name of a schema file (excluding .json) which is located in the `./schemas/` directory. Once the schema is entered, an SQL file will be generated and will be executed on the database. Finally, the database will be made no longer publicly available in AWS.

#### Using !create without config
![!create command demo without config](/demos/demo-create-without-config.gif)

The `!create` command will initially ask if you want to create with or without a config, type 'n' to create without a config. You will be asked to enter the bare minimum of values required to create an RDS instance. Then, you will have a chance to confirm your configuration. Upon confirmation, the database will be created. Once the database status is `Available`, you will be prompted to enter the name of a schema file (excluding .json) which is located in the `./schemas/` directory. Once the schema is entered, an SQL file will be generated and will be executed on the database. Finally, the database will be made no longer publicly available in AWS.

#### Using !more during !create
![!more during !create](/demos/demo-using-more.gif)

The `!more` command will print a description and valid values for the option you are being prompted during !create (without config).
