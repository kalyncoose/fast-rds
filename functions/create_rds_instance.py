"""
     ___   ____           __                 __        ___
    / _/  / ______ ______/ /_      _________/ _____   /  /
   / /   / /_/ __ `/ ___/ ________/ ___/ __  / ___/   / / 
  / /   / __/ /_/ (__  / /_/_____/ /  / /_/ (__  )   / /  
 / /   /_/  \__,_/____/\__/     /_/   \__,_/____/  _/ /   
/__/   https://github.com/kalyncoose/fast-rds     /__/    

Provided by Apache 2.0 License
See requirements.txt for other packages and their licenses.
"""

import boto3
import re
from functions import check_rds_instance as cri

# create_rds_instance(str, dict):
# creates the RDS instance based on the
# config dict provided and pass along
# connection attributes to the
# check_rds_instance() function.
def create_rds_instance(auto_name, **kwargs):

    # Create RDS client
    rds = boto3.client('rds')
    response = rds.create_db_instance(**kwargs)

    # Check ResponseMetadata for 200 code
    if response.get('ResponseMetadata').get('HTTPStatusCode') == 200:
        # Set default instance states
        states = ['Creating', 'Back-Up', 'Available']
        
        # Store important connection information for later
        connection = {}
        connection['MasterUsername'] = kwargs.get('MasterUsername')
        connection['MasterUserPassword'] = kwargs.get('MasterUserPassword')
        connection['DBName'] = kwargs.get('DBName')
        connection['Port'] = kwargs.get('Port')

        # Update states if configuration has these enabled
        if kwargs.get('EnablePerformanceInsights', False):
            states.append('Configuring-Enhanced-Monitoring')
        if kwargs.get('EnableCloudwatchLogsExports', []):
            states.append('Configuring-Log-Exports')
        
        # Call check_rds_instance() to print a progress bar to console and continuously check instance status
        cri.check_rds_instance(kwargs.get('DBInstanceIdentifier'), states, connection, auto_name)