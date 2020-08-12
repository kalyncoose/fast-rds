from functions import modify_rds_instance as mri

rds_name = 'fast-rds-automated'
schema_name = 'example'
endpoint = 'fast-rds-automated.cnyxgdigzo3g.us-east-2.rds.amazonaws.com'
connection = {
    "Port": 5432,
    'MasterUsername': 'postgres',
    'MasterUserPassword': 'password',
    'DBName': 'example'
}

mri.modify_rds_instance(rds_name, schema_name, endpoint, connection)