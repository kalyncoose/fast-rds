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
import time
from colorama import init, Fore, Back, Style
from progress.bar import IncrementalBar
from functions import create_postgres_sql as cps
init(convert=True)

# Tag
tag = Style.BRIGHT + Fore.BLUE + '[fast-rds] ' + Fore.RESET

# Global Variables
creating = False
backing_up = False
available = False
monitoring = False
logging = False
count = 0

# check_rds_instance(str, list, dict, str):
# prints a progress bar to console and updates
# the RDS instance status as it is being created,
# then calls create_postgres_sql() to generate sql files.
def check_rds_instance(rds_name, states, connection, auto_name):
    
    # Create RDS client
    rds = boto3.client('rds')
    print('\n' + tag + 'Creating Database\nPlease wait as it typically takes 10-15 minutes before an instance is available.')
    
    # Create progress bar and continuously update it
    bar = IncrementalBar(rds_name, max=len(states), suffix='')
    while True:
        global creating
        global backing_up
        global available
        global monitoring
        global logging
        global count
        
        # Check RDS instance
        response = rds.describe_db_instances(DBInstanceIdentifier=rds_name)
        instances = response.get('DBInstances')
        status = instances[0].get('DBInstanceStatus').title()
        
        # Handle 'Creating' status
        if status == 'Creating' and not creating:
            creating = True
            bar.next()
            count += 1
            print(str(count) + '/' + str(len(states)) + ' | Status: ' + status, end='\r', flush=True)
        
        # Handle 'Backing-Up' status
        elif status == 'Backing-Up' and not backing_up:
            backing_up = True
            bar.next()
            count += 1
            print(str(count) + '/' + str(len(states)) + ' | Status: ' + status, end='\r', flush=True)
        
        # Handle 'Available' status
        elif status == 'Available' and not available:
            available = True
            bar.next()
            count += 1
            print(str(count) + '/' + str(len(states)) + ' | Status: ' + status, end='\r', flush=True)
            break
        
        # Handle 'Configuring-Enhanced-Monitoring' status
        elif status == 'Configuring-Enhanced-Monitoring' and not monitoring:
            monitoring = True
            bar.next()
            count += 1
            print(str(count) + '/' + str(len(states)) + ' | Status: ' + status, end='\r', flush=True)
        
        # Handle 'Configuring-Log-Exports' status
        elif status == 'Configuring-Log-Exports' and not logging:
            logging = True
            bar.next()
            count += 1
            print(str(count) + '/' + str(len(states)) + ' | Status: ' + status, end='\r', flush=True)
        
        # Sleep for 30 seconds between checks
        time.sleep(30)

    # Finish progress bar
    bar.finish()

    # Check for schema and grab endpoint
    check_schema = False
    while not check_schema:
        
        # Automatically create postgresql based on auto_name
        if auto_name:
            check_schema = True
            response = rds.describe_db_instances(DBInstanceIdentifier=rds_name)
            instances = response.get('DBInstances')
            endpoint = instances[0].get('Endpoint').get('Address')
            
            cps.create_postgres_sql(rds_name, auto_name, endpoint, connection)
        
        # Ask for schema file if auto_name not provided
        else:
            print('\n' + tag + 'Database Ready\n' + 'Please specify the schema filename (excluding .json):', end=' ')
            schema_name = input()
            if schema_name != '' and not schema_name.endswith('.json'):
                check_schema = True

                response = rds.describe_db_instances(DBInstanceIdentifier=rds_name)
                instances = response.get('DBInstances')
                endpoint = instances[0].get('Endpoint').get('Address')

                cps.create_postgres_sql(rds_name, schema_name, endpoint, connection)
            
            # Handle invalid input
            else:
                print(Style.BRIGHT + 'Invalid entry. Please enter a valid schema filename exlcuding the ".json" extension.\n')