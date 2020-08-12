import boto3
import re
from functions import check_rds_instance as cri

def create_rds_instance(auto_name, **kwargs):

    rds = boto3.client('rds')
    response = rds.create_db_instance(**kwargs)

    if response.get('ResponseMetadata').get('HTTPStatusCode') == 200:
        states = ['Creating', 'Back-Up', 'Available']
        connection = {}

        connection['MasterUsername'] = kwargs.get('MasterUsername')
        connection['MasterUserPassword'] = kwargs.get('MasterUserPassword')
        connection['DBName'] = kwargs.get('DBName')
        connection['Port'] = kwargs.get('Port')

        if kwargs.get('EnablePerformanceInsights', False):
            states.append('Configuring-Enhanced-Monitoring')
        if kwargs.get('EnableCloudwatchLogsExports', []):
            states.append('Configuring-Log-Exports')
        
        cri.check_rds_instance(kwargs.get('DBInstanceIdentifier'), states, connection, auto_name)