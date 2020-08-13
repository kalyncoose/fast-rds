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

import json
from functions import modify_rds_instance as mri

# Global Variables
field_name = None
field_type = None
primary_key = None
unique = None
not_null = None
personal_data = None
default = None

# create_postgres_sql(str, str, str, dict):
# generates a sql file in the ./SQLs/ directory
# based on the provided schema_name file,
# then calls modify_rds_instance() to connect
# to the database and execute the sql file.
def create_postgres_sql(rds_name, schema_name, endpoint, connection):

    # Open ./schemas/"schema_name".json file
    with open('./schemas/' + schema_name + '.json', "r") as read_file:
        schema_file = json.load(read_file)
        
        # Create new ./SQLs/"schema_name".sql file
        sql = open('./SQLs/' + schema_name + '.sql', "w+")
        
        # Write beginning comment and extension creation for uuid
        sql.write('-- Create new table for ' + schema_name + ' database\n')
        sql.write('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";\n')
        
        # Iterate through schema_file
        for item in schema_file.items():
            
            # Handle 'table' in schema
            if item[0] == 'table':
                keys = []
                comments = []
                sql.write('CREATE TABLE IF NOT EXISTS ' + schema_name + ' (\n')
                #print(item[1]) # DEBUG
                
                # Handle each 'field' in 'table' schema
                for field in item[1]:
                    #print(field)   # DEBUG

                    # Update Global Variables
                    global field_name
                    global field_type
                    global primary_key
                    global unique
                    global not_null
                    global personal_data
                    global default

                    # Set each value or set = None
                    if field.get('field'):
                        field_name = field.get('field')
                        #print(field_name)  # DEBUG
                    else:
                        field_name = None
                    
                    if field.get('type'):
                        field_type = field.get('type')
                        #print(field_type)  # DEBUG
                    else:
                        field_type = None
                    
                    if field.get('primary_key'):
                        primary_key = field
                        #print(primary_key) # DEBUG
                    else:
                        primary_key = None
                    
                    if field.get('unique'):
                        unique = field.get('unique')
                        #print(unique)  # DEBUG
                    else:
                        unique = None
                    
                    if field.get('not_null'):
                        not_null = field.get('not_null')
                        #print(not_null)    # DEBUG
                    else:
                        not_null = None
                    
                    if field.get('personal_data'):
                        personal_data = field.get('personal_data')
                        #print(personal_data)   # DEBUG
                    else:
                        personal_data = None
                    
                    if field.get('default'):
                        default = field.get('default')
                        #print(default) # DEBUG
                    else:
                        default = None

                    # Write each field content to sql file
                    sql.write('\t' + field_name)

                    if field_type == 'uuid':
                        sql.write(' uuid DEFAULT uuid_generate_v4()')

                    if field_type == 'text':
                        sql.write(' VARCHAR(50)')

                    if field_type == 'boolean':
                        sql.write(' BOOLEAN')

                    if field_type == 'date':
                        sql.write(' TIMESTAMPTZ')

                    if primary_key:
                        keys.append('\tPRIMARY KEY ('+field_name+')\n')

                    if unique:
                        sql.write(' UNIQUE')

                    if not_null:
                        sql.write(' NOT NULL')
                    
                    if default:
                        if field_type == 'boolean':
                            temp = str(default).lower()
                            sql.write(' DEFAULT \'' + temp[0] + '\'')
                        else:
                            sql.write(' DEFAULT '+str(default))
                    
                    if personal_data:
                        comments.append('COMMENT ON COLUMN '+schema_name+'.'+field_name+' IS \'personal_data\';\n')
                    
                    sql.write(',\n')

                # Write any primary keys to end of table creation
                for key in keys:
                    sql.write(key)
                sql.write(');\n')

                # Write any comments outside of table creation
                for comment in comments:
                    sql.write(comment)

            # Write description at the end
            if item[0] == 'description':
                sql.write('COMMENT ON TABLE '+schema_name+' IS \''+item[1]+'\';\n')

        # Close the sql file
        sql.close()

        # Call modify_rds_instance to connect to the database and execute the SQL file
        mri.modify_rds_instance(rds_name, schema_name, endpoint, connection)