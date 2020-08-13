# fast-rds

The purpose of fast-rds is to streamline Amazon Web Services' RDS database creation using code generation based on a provided schema.

## Demos

### !automate command
 ![!automate command demo](/demo-automate.gif)
 ![Resulting database in RDS](/demo-automate.png)
 The `!automate [option]` command will create an RDS instance from the specified `[option].json` in ./configs/ directory and generate an SQL file based on the specified `[option].json` in ./schemas/ directory. Therefore, **both `.json` files require the same name** for the `!automate` command to work.
 
### !create command

### !help command

## Getting Started

### Prerequisites

In order to run fast-rds, you must have the latest AWS CLI version installed and configured.

[You may select and install AWS CLI here.](https://aws.amazon.com/cli/)

To configure your AWS CLI, use `aws configure` once installed.

**Note:** It is recommended that you configure your AWS CLI based on an IAM user's security credentials.
