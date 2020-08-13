"""
     ___   ____           __                 __        ___
    / _/  / ______ ______/ /_      _________/ _____   /  /
   / /   / /_/ __ `/ ___/ ________/ ___/ __  / ___/   / / 
  / /   / __/ /_/ (__  / /_/_____/ /  / /_/ (__  )   / /  
 / /   /_/  \__,_/____/\__/     /_/   \__,_/____/  _/ /   
/__/   https://github.com/kalyncoose/fast-rds     /__/    

Copyright 2020 Kalyn Coose

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

See requirements.txt for other packages and their licenses.
"""

import boto3
import psycopg2
from colorama import init, Fore, Back, Style
init(convert=True)

# Tag
tag = Style.BRIGHT + Fore.BLUE + '[fast-rds] ' + Fore.RESET

# modify_rds_instance(str, str, str, dict):
# connects to the database and executes the
# previously generated SQL file, then modifies
# the database to be no longer publicly
# accessible in AWS.
def modify_rds_instance(rds_name, schema_name, endpoint, connection):
    print('\n' + tag + 'Connecting to Database')
    #print(connection)  # DEBUG
    
    # Connect to database
    conn = psycopg2.connect(
        host = endpoint,
        port = int(connection.get('Port')),
        user = connection.get('MasterUsername'),
        password = connection.get('MasterUserPassword'),
        database = connection.get('DBName')
    )

    print('\n' + tag + 'Executing SQL on Database')

    # Create database cursor with connection
    with conn:
        with conn.cursor() as cursor:
            
            # Execute ./SQLs/"schema_name".sql file
            cursor.execute(open("./SQLs/"+schema_name+'.sql', "r").read())
            
            # Execute SELECT statement to retrieve new table information
            cursor.execute("SELECT * FROM "+schema_name)
            
            # Obtain column names from cursor
            colnames = [desc[0] for desc in cursor.description]
            #rows = cursor.fetchall()   # DEBUG
            
            # Print select statement to simulate pg-admin
            print('\n'+connection.get('DBName')+" => SELECT * FROM "+schema_name+";\n")
            for col in colnames:
                if colnames[len(colnames)-1] == col:
                    print(col)
                else:
                    print(col+' | ', end='')
            print('----------------------------------------------------\n')
            print('(' + str(len(colnames)) + ' columns, 0 rows)')
    
    # Create RDS client and modify instance to be no longer publicly accessible
    rds = boto3.client('rds')
    response = rds.modify_db_instance(DBInstanceIdentifier=rds_name, PubliclyAccessible=False)
    
    # Retrieve ResponseMetadata for 200 code
    if response.get('ResponseMetadata').get('HTTPStatusCode') == 200:
        print('\n' + tag + 'Database is no longer publicly accessible.')