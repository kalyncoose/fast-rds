# fast-rds

fast-rds is a proof-of-concept tool designed to streamline database creation using configuration and schema files, which are in turn used in code generating SQL files that are executed immediately on the database.

## Demos

### !automate command
 ![!automate command demo](/demo-automate.gif)
 ![Resulting database in RDS](/demo-automate.png)
 The `!automate [option]` command will create the database given the config JSON file in the `./configs/` directory. Then, once the database status is `Available`, it will generate an SQL file based on the JSON schema file in the `./schemas/` directory. Once the SQL is generated, it will execute it on the database and then make the database no longer publicly accessible in AWS.
 
### !create command

### !help command

## Getting Started

### Prerequisites

In order to run fast-rds, you must have the latest AWS CLI version installed and configured.

[You may select and install AWS CLI here.](https://aws.amazon.com/cli/)

To configure your AWS CLI, use `aws configure` once installed.

**Note:** It is recommended that you configure your AWS CLI based on an IAM user's security credentials.
