import boto3
import psycopg2
from colorama import init, Fore, Back, Style
init(convert=True)

tag = Style.BRIGHT + Fore.BLUE + '[fast-rds] ' + Fore.RESET

def modify_rds_instance(rds_name, schema_name, endpoint, connection):

    print('\n' + tag + 'Connecting to Database')
    #print(connection)
    conn = psycopg2.connect(
        host = endpoint,
        port = int(connection.get('Port')),
        user = connection.get('MasterUsername'),
        password = connection.get('MasterUserPassword'),
        database = connection.get('DBName')
    )

    print('\n' + tag + 'Executing SQL on Database')

    with conn:
        with conn.cursor() as cursor:
            cursor.execute(open("./SQLs/"+schema_name+'.sql', "r").read())
            cursor.execute("SELECT * FROM "+schema_name)
            colnames = [desc[0] for desc in cursor.description]
            #rows = cursor.fetchall()
            print('\n'+connection.get('DBName')+" => SELECT * FROM "+schema_name+";\n")
            for col in colnames:
                if colnames[len(colnames)-1] == col:
                    print(col)
                else:
                    print(col+' | ', end='')
            print('----------------------------------------------------\n')
            print('(' + str(len(colnames)) + ' columns, 0 rows)')
    
    rds = boto3.client('rds')
    response = rds.modify_db_instance(DBInstanceIdentifier=rds_name, PubliclyAccessible=False)
    if response.get('ResponseMetadata').get('HTTPStatusCode') == 200:
        print('\n' + tag + 'Database is no longer publicly accessible.')