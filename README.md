# fast-rds

fast-rds is a proof-of-concept CLI tool designed to streamline [AWS RDS](https://aws.amazon.com/rds/) database creation using configuration files and code generation.

## Demo

### !automate command
 ![!automate command demo](/demos/demo-automate.gif)
 ![Resulting database in RDS](/demos/demo-automate.png)

The `!automate [option]` command will create the database given the config JSON file in the `./configs/` directory. Then, once the database status is `Available`, it will generate an SQL file based on the JSON schema file in the `./schemas/` directory. Once the SQL is generated, it will execute it on the database and then make the database no longer publicly accessible in AWS.

### Instance Configuration
When automated, the database instance is configured with the values from a file in the `./configs/` directory.

Example:
```json
{
    "DBInstanceIdentifier": "my-example-db",
    "DBInstanceClass": "db.t2.micro",
    "Engine": "postgres",
    "Port": 5432,
    "StorageType": "gp2",
    "AllocatedStorage": 100,
    "DBName": "test",
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

#### Requirements Installation

Run the following to install all the requirements:
```
pip install -r requirements.txt
```

Explanation of Package Usage:
* `boto3` - Use AWS in Python
* `psycopg2` - Connect and Execute Postgresql in Python
* `progress` - Progress/Loading Bar
* `colorama` - Text color support for Windows Command Prompt/Linux Terminals
* `js-regex` - Use JavaScript regex in Python

#### Copy and Modify Example Files

Once your project is ready to run, copy the `example.json` file in both `./configs/` and `./schemas/` then rename and modify the values to your preference.

### Run the Project

While in the directory of `fast_rds.py`, run the project using `python.exe fast_rds.py [command] [option]`.

Currently, these are the supported commands:
* `!automate [option]` - Where option is the name of the config and schema file excluding the .json extension.
* `!create` - There are no options needed, this command provides the same functionality as `!automate [option]` but is a more hand-held experience.
* `!more` - This command is only used when prompted for input during the `!create` command.

See the section below for more information.

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

## To Do

### Missing Features

#### More DB Engine Support

This tool currently only supports generating SQL files for a Postgresql database. However, the `!create` command is perfect for creating RDS databases with the other available engine types.

#### Security Group Creation and Modification

This tool currently allows you to pass a pre-defined security group in the `./configs/` file. However, a new feature could generate a new security group with inbound traffic open so that the SQL can be executed and after execution the security group could be modified to remove inbound traffic accessibility.

#### More?

Please let me know if any more features should be added.
