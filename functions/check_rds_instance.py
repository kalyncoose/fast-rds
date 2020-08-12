import boto3
import time
from colorama import init, Fore, Back, Style
from progress.bar import IncrementalBar
from functions import create_postgres_sql as cps
init(convert=True)

tag = Style.BRIGHT + Fore.BLUE + '[fast-rds] ' + Fore.RESET
creating = False
backing_up = False
available = False
monitoring = False
logging = False
count = 0

def check_rds_instance(rds_name, states, connection, auto_name):
    rds = boto3.client('rds')
    print('\n' + tag + 'Creating Database\nPlease wait as it typically takes 10-15 minutes before an instance is available.')
    bar = IncrementalBar(rds_name, max=len(states), suffix='')
    while True:
        global creating
        global backing_up
        global available
        global monitoring
        global logging
        global count
        
        response = rds.describe_db_instances(DBInstanceIdentifier=rds_name)
        instances = response.get('DBInstances')
        status = instances[0].get('DBInstanceStatus').title()
        if status == 'Creating' and not creating:
            creating = True
            bar.next()
            count += 1
            print(str(count) + '/' + str(len(states)) + ' | Status: ' + status, end='\r', flush=True)
        elif status == 'Backing-Up' and not backing_up:
            backing_up = True
            bar.next()
            count += 1
            print(str(count) + '/' + str(len(states)) + ' | Status: ' + status, end='\r', flush=True)
        elif status == 'Available' and not available:
            available = True
            bar.next()
            count += 1
            print(str(count) + '/' + str(len(states)) + ' | Status: ' + status, end='\r', flush=True)
            break
        elif status == 'Configuring-Enhanced-Monitoring' and not monitoring:
            monitoring = True
            bar.next()
            count += 1
            print(str(count) + '/' + str(len(states)) + ' | Status: ' + status, end='\r', flush=True)
        elif status == 'Configuring-Log-Exports' and not logging:
            logging = True
            bar.next()
            count += 1
            print(str(count) + '/' + str(len(states)) + ' | Status: ' + status, end='\r', flush=True)
        time.sleep(30)
    bar.finish()

    check_schema = False
    while not check_schema:

        if auto_name:
            check_schema = True
            response = rds.describe_db_instances(DBInstanceIdentifier=rds_name)
            instances = response.get('DBInstances')
            endpoint = instances[0].get('Endpoint').get('Address')
            
            cps.create_postgres_sql(rds_name, auto_name, endpoint, connection)
        else:
            print('\n' + tag + 'Database Ready\n' + 'Please specify the schema filename (excluding .json):', end=' ')
            schema_name = input()
            if schema_name != '' and not schema_name.endswith('.json'):
                check_schema = True

                response = rds.describe_db_instances(DBInstanceIdentifier=rds_name)
                instances = response.get('DBInstances')
                endpoint = instances[0].get('Endpoint').get('Address')

                cps.create_postgres_sql(rds_name, schema_name, endpoint, connection)
            else:
                print(Style.BRIGHT + 'Invalid entry. Please enter a valid schema filename exlcuding the ".json" extension.\n')