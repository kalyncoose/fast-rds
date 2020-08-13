# fast-rds

`[fast-rds]` is a proof-of-concept tool designed to streamline database creation using a configuration file and code generation to create and execute SQL based on a provided schema.

## Demos

### !automate command
 ![!automate command demo](/demos/demo-automate.gif)
 ![Resulting database in RDS](/demos/demo-automate.png)

The `!automate [option]` command will create the database given the config JSON file in the `./configs/` directory. Then, once the database status is `Available`, it will generate an SQL file based on the JSON schema file in the `./schemas/` directory. Once the SQL is generated, it will execute it on the database and then make the database no longer publicly accessible in AWS.
 
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

## Getting Started

### Prerequisites

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
