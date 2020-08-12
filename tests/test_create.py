from functions import create_postgres_sql as cps

rds_name = 'test'
schema_name = 'example'
endpoint = 'test.cnyxgdigzo3g.us-east-2.rds.amazonaws.com'
connection = {
    "Port": 5432,
    'MasterUsername': 'postgres',
    'MasterUserPassword': 'password',
    'DBName': 'example'
}

cps.create_postgres_sql(rds_name, schema_name, endpoint, connection)