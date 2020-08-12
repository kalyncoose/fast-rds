import json
from functions import modify_rds_instance as mri

field_name = None
field_type = None
primary_key = None
unique = None
not_null = None
personal_data = None
default = None

def create_postgres_sql(rds_name, schema_name, endpoint, connection):

    with open('./schemas/' + schema_name + '.json', "r") as read_file:
        schema_file = json.load(read_file)
        sql = open('./SQLs/' + schema_name + '.sql', "w+")
        sql.write('-- Create new table for ' + schema_name + ' database\n')
        sql.write('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";\n')
        for item in schema_file.items():
            if item[0] == 'table':
                keys = []
                comments = []
                sql.write('CREATE TABLE IF NOT EXISTS ' + schema_name + ' (\n')
                #print(item[1])
                for field in item[1]:
                    #print(field)
                    global field_name
                    global field_type
                    global primary_key
                    global unique
                    global not_null
                    global personal_data
                    global default

                    if field.get('field'):
                        field_name = field.get('field')
                        #print(field_name)
                    else:
                        field_name = None
                    
                    if field.get('type'):
                        field_type = field.get('type')
                        #print(field_type)
                    else:
                        field_type = None
                    
                    if field.get('primary_key'):
                        primary_key = field
                        #print(primary_key)
                    else:
                        primary_key = None
                    
                    if field.get('unique'):
                        unique = field.get('unique')
                        #print(unique)
                    else:
                        unique = None
                    
                    if field.get('not_null'):
                        not_null = field.get('not_null')
                        #print(not_null)
                    else:
                        not_null = None
                    
                    if field.get('personal_data'):
                        personal_data = field.get('personal_data')
                        #print(personal_data)
                    else:
                        personal_data = None
                    
                    if field.get('default'):
                        default = field.get('default')
                        #print(default)
                    else:
                        default = None

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

                for key in keys:
                    sql.write(key)
                sql.write(');\n')
                for comment in comments:
                    sql.write(comment)

            if item[0] == 'description':
                sql.write('COMMENT ON TABLE '+schema_name+' IS \''+item[1]+'\';\n')

        sql.close()

        mri.modify_rds_instance(rds_name, schema_name, endpoint, connection)