import sys
import re
import js_regex
from colorama import init, Fore, Back, Style
init(convert=True)
from functions import create_rds_instance as cri

# Tag & Options
tag = Style.BRIGHT + Fore.BLUE + '[fast-rds] ' + Fore.RESET
options = Style.BRIGHT + Fore.GREEN + ' [y]' + Fore.RED + '[n]' + Fore.YELLOW + '[!more]' + Fore.RESET + ': '

# Config Dict
config = {
    'DBName': '',
    'DBInstanceIdentifier': '',
    'AllocatedStorage': '',
    'DBInstanceClass': '',
    'Engine': '',
    'MasterUsername': '',
    'MasterUserPassword': '',
    'Port': '',
    'Iops': '',
    'StorageType': '',
}

def create_without_config():
    print('\n' + tag + 'Create Without Config File\n' +
            'Please enter values for the following configurations...\n' +
            'For each entry, type ' + Fore.YELLOW + '!more' + Fore.RESET + ' for more information.')

    # RDS Instance Name
    check_rds_instance_name = False
    while not check_rds_instance_name:
        print('\n' + tag + 'RDS Instance Name:', end=' ')
        rds_name = input()
        if js_regex.compile("^(?:[a-z]|[a-z][a-z0-9]{1,62}|[a-z](?:[a-z0-9]|\-(?!\-)){1,61}[a-z0-9])$").search(rds_name):
            check_rds_instance_name = True
            config['DBInstanceIdentifier'] = rds_name
        elif rds_name.lower().startswith('!more'):
            print('\n' + tag + 'RDS Instance Name\n' + 'The DB instance identifier. This parameter is stored as a lowercase string.\n' +
                    '\nConstraints:\n' +
                    '- Must contain from 1 to 63 letters, numbers, or hyphens\n' +
                    '- First character must be a letter\n' + 
                    '- Cannot end with a hypen or contain two consecutive hypens')
        else:
            print(Style.BRIGHT + 'Invalid entry. Type ' + Fore.YELLOW + '!more' + Fore.RESET + ' for more information.')
    
    # Database Engine
    check_db_engine = False
    while not check_db_engine:
        print('\n' + tag + 'Database Engine:', end=' ')
        db_engine = input()
        if (db_engine == "aurora"
            or db_engine == "aurora-mysql"
            or db_engine == "aurora-postgresql"
            or db_engine == "mariadb"
            or db_engine == "mysql"
            or db_engine == "oracle-ee" 
            or db_engine == "oracle-se" 
            or db_engine == "oracle-se1"
            or db_engine == "oracle-se2"
            or db_engine == "postgres"
            or db_engine == "sqlserver-ee" 
            or db_engine == "sqlserver-se"
            or db_engine == "sqlserver-ex" 
            or db_engine == "sqlserver-web"):
            check_db_engine = True
            config['Engine'] = db_engine
        elif db_engine.lower().startswith('!more'):
            print('\n' + tag + 'Database Engine\n' + 'The name of the database engine to be used for this instance.\n' +
                    'Not every database engine is available for every AWS Region.\n' +
                    '\nValid Values:\n' +
                    '- aurora (for MySQL 5.6-compatible Aurora)\n' +
                    '- aurora-mysql (for MySQL 5.7-compatible Aurora)\n' +
                    '- aurora-postgresql\n' +
                    '- mariadb\n' +
                    '- mysql\n' +
                    '- oracle-ee\n' +
                    '- oracle-se\n' +
                    '- oracle-se1\n' +
                    '- oracle-se2\n' +
                    '- postgres\n' +
                    '- sqlserver-ee\n' +
                    '- sqlserver-se\n' +
                    '- sqlserver-ex\n' +
                    '- sqlserver-web')
        else:
            print(Style.BRIGHT + 'Invalid entry. Type ' + Fore.YELLOW + '!more' + Fore.RESET + ' for more information.')

    # Database Name
    check_db_name = False
    while not check_db_name:
        print('\n' + tag + 'Database Name:', end=' ')
        db_name = input()
        if re.search(r'^[a-zA-Z0-9\_]{1,63}', db_name):
            check_db_name = True
            config['DBName'] = db_name
        elif db_name.lower().startswith('!more'):
            print('\n' + tag + 'Database Name\n' + 'The name of the database to create when the DB instance is created.\n' +
                    '\nConstraints:\n' +
                    '- Must contain 1 to 63 letters, number, or underscores\n' +
                    '- Must begin with a letter or an underscore\n' +
                    '- Subsequent characters can be letters, underscores, or digits (0-9)\n' +
                    '- Cannot be a word reserved by the specified database engine')
        else:
            print(Style.BRIGHT + 'Invalid entry. Type ' + Fore.YELLOW + '!more' + Fore.RESET + ' for more information.')

    # Database Port
    check_db_port = False
    while not check_db_port:
        print('\n' + tag + 'Database Port:', end=' ')
        db_port = input()
        if db_port.isdigit() and 1150 <= int(db_port) <= 65535:
            check_db_port = True
            config['Port'] = int(db_port)
        elif db_port.lower().startswith('!more'):
            print('\n' + tag + 'Database Port\n' + 'The port number on which the database accepts connections.\n' +
                    '\nValid Values:\n' +
                    '- 1550-65535\n' +
                    '\nDefault Values:\n' +
                    '- mysql: 3306\n' +
                    '- mariadb: 3306\n' +
                    '- postgres: 5432\n' +
                    '- oracle: 1521\n' +
                    '- sqlserver: 1433\n' + 
                    '- aurora: 3306')
        else:
            print(Style.BRIGHT + 'Invalid entry. Type ' + Fore.YELLOW + '!more' + Fore.RESET + ' for more information.')
    
    # Database Class
                    # db.m5 – Latest Generation Memory Optimized Instance Classes
    db_classes = ['db.m5.24xlarge', 'db.m5.16xlarge', 'db.m5.12xlarge', 'db.m5.8xlarge', 'db.m5.4xlarge', 'db.m5.2xlarge', 'db.m5.xlarge', 'db.m5.large',
                    # db.m4 – Current Generation Standard Instance Classes
                    'db.m4.16xlarge', 'db.m4.10xlarge', 'db.m4.4xlarge', 'db.m4.2xlarge', 'db.m4.xlarge', 'db.m4.large',
                    # db.r3 – Previous Generation Memory Optimized Instance Classes
                    'db.m3.2xlarge', 'db.m3.xlarge', 'db.m3.large', 'db.m3.medium',
                    # db.r4 – Current Generation Memory Optimized Instance Classes
                    'db.r4.16xlarge', 'db.r4.8xlarge', 'db.r4.4xlarge', 'db.r4.2xlarge', 'db.r4.xlarge', 'db.r4.large',
                    # db.t3 – Latest Generation Burstable Performance Instance Classes
                    'db.t3.2xlarge', 'db.t3.xlarge', 'db.t3.large', 'db.t3.medium', 'db.t3.small', 'db.t3.micro',
                    # db.t2 – Current Generation Burstable Performance Instance Classes
                    'db.t2.2xlarge', 'db.t2.xlarge', 'db.t2.large', 'db.t2.medium', 'db.t2.small', 'db.t2.micro']
    check_db_class = False
    while not check_db_class:
        print('\n' + tag + 'Database Instance Class:', end=' ')
        db_class = input()
        if db_class in db_classes:
            check_db_class = True
            config['DBInstanceClass'] = db_class
        elif db_class.lower().startswith('!more'):
            print('\n' + tag + 'The compute and memory capacity of the DB instance.\n' +
                    'Not all DB instance classes are available in all AWS Regions\n' +
                    'or for all database engines.\n' +
                    '\nCurrent supported classes:\n' + 
                    Fore.CYAN + 'db.m5 – Latest Generation Memory Optimized Instance Classes:\n' + Fore.RESET +
                    '- db.m5.24xlarge\n' +
                    '- db.m5.16xlarge\n' +
                    '- db.m5.12xlarge\n' +
                    '- db.m5.8xlarge\n' +
                    '- db.m5.4xlarge\n' +
                    '- db.m5.2xlarge\n' +
                    '- db.m5.xlarge\n' +
                    '- db.m5.large\n' +
                    Fore.CYAN + 'db.m4 – Current Generation Standard Instance Classes:\n' + Fore.RESET +
                    '- db.m4.16xlarge\n' +
                    '- db.m4.10xlarge\n' +
                    '- db.m4.4xlarge\n' +
                    '- db.m4.2xlarge\n' +
                    '- db.m4.xlarge\n' +
                    '- db.m4.large\n' +
                    Fore.CYAN + 'db.r3 – Previous Generation Memory Optimized Instance Classes:\n' + Fore.RESET +
                    '- db.m3.2xlarge\n' +
                    '- db.m3.xlarge\n' +
                    '- db.m3.large\n' +
                    '- db.m3.medium\n' +
                    Fore.CYAN + 'db.r4 – Current Generation Memory Optimized Instance Classes:\n' + Fore.RESET +
                    '- db.r4.16xlarge\n' +
                    '- db.r4.8xlarge\n' +
                    '- db.r4.4xlarge\n' +
                    '- db.r4.2xlarge\n' +
                    '- db.r4.xlarge\n' +
                    '- db.r4.large\n' +
                    Fore.CYAN + 'db.t3 – Latest Generation Burstable Performance Instance Classes:\n' + Fore.RESET +
                    '- db.t3.2xlarge\n' +
                    '- db.t3.xlarge\n' +
                    '- db.t3.large\n' +
                    '- db.t3.medium\n' +
                    '- db.t3.small\n' +
                    '- db.t3.micro\n' +
                    Fore.CYAN + 'db.t2 – Current Generation Burstable Performance Instance Classes:\n' + Fore.RESET +
                    '- db.t2.2xlarge\n' +
                    '- db.t2.xlarge\n' +
                    '- db.t2.large\n' +
                    '- db.t2.medium\n' +
                    '- db.t2.small\n' +
                    '- db.t2.micro')
        else:
            print(Style.BRIGHT + 'Invalid entry. Type ' + Fore.YELLOW + '!more' + Fore.RESET + ' for more information.')

    # Database Storage Type
    check_db_storage_type = False
    while not check_db_storage_type:
        print('\n' + tag + 'Storage Type [gp2][io1][standard]:', end=' ')
        db_storage_type = input()
        if db_storage_type == 'gp2' or db_storage_type == 'io1' or db_storage_type == 'standard':
            check_db_storage_type = True
            config['StorageType'] = db_storage_type
        elif db_storage_type.lower().startswith('!more'):
            print('\n' + tag + 'Database Storage Type\n' + 'Specifies the storage type to be associated with the DB instance.\n' +
                    '\nValid Values:\n' +
                    '- gp2 (General Purpose SSD)\n' +
                    '- io1 (Provisioned IOPS storage)\n' +
                    '- standard (Magnetic storage)')
        else:
            print(Style.BRIGHT + 'Invalid entry. Type ' + Fore.YELLOW + '!more' + Fore.RESET + ' for more information.')

    # Database Storage Size
    check_db_storage_size = False
    while not check_db_storage_size:
        print('\n' + tag + 'Storage Size (GiB): ', end=' ')
        db_storage_size = input()
        if db_storage_size.isdigit() and (5 <= int(db_storage_size) <= 65536):
            check_db_storage_size = True
            config['AllocatedStorage'] = int(db_storage_size)
        elif db_storage_size.lower().startswith('!more'):
            print('\n' + tag + 'Database Storage Size\n' + 'Constraints to the amount of storage (in Gibibytes) of each storage type are the following:\n' +
                    '- General Purpose (SSD) storage (gp2): 20 to 65536\n' +
                    '- Provisioned IOPS storage (io1): 100 to 65536\n' +
                    '- Magnetic storage (standard): 5 to 3072')
        else:
            print(Style.BRIGHT + 'Invalid entry. Type ' + Fore.YELLOW + '!more' + Fore.RESET + ' for more information.')

    # IOPS Value
    check_iops_value = False
    while not check_iops_value:
        if db_storage_type != 'io1':
            check_iops_value = True
        else:
            print('\n' + tag + 'IOPS Value:', end=' ')
            iops_value = input()
            if iops_value.isdigit() and (1000 <= int(iops_value) <= 40000):
                check_iops_value = True
                config['Iops'] = int(iops_value)
            elif iops_value.lower().startswith('!more'):
                print('\n' + tag + 'IOPS Value\n' + 'The amount of Provisioned IOPS (input/output operations per second) to be allocated for the DB instance.\n' +
                        '\nConstraints: For mariadb, mysql, oracle, and postgres instances, IOPS must be a multiple between\n' +
                        '0.5 and 50 of the storage amount for the DB instance.\n' + 
                        '\nValid Values:\n' + 
                        '- 1000 to 40000')
            else:
                print(Style.BRIGHT + 'Invalid entry. Type ' + Fore.YELLOW + '!more' + Fore.RESET + ' for more information.')

    # Database Master Username
    check_db_master_username = False
    while not check_db_master_username:
        print('\n' + tag + 'Database Master Username:', end=' ')
        db_master_username = input()
        if re.search(r'^[a-zA-Z0-9]{1,20}', db_master_username):
            check_db_master_username = True
            config['MasterUsername'] = db_master_username
        elif db_master_username.lower().startswith('!more'):
            print('\n' + tag + 'Database Master Username\n' + 'The name for the master user.\n' +
                    '\nConstraints:\n' +
                    '- Must be 1 to 20 letters or numbers\n' +
                    '- Cannot be a reserved word for the chosen database engine')
        else:
            print(Style.BRIGHT + 'Invalid entry. Type ' + Fore.YELLOW + '!more' + Fore.RESET + ' for more information.')
    
    # Database Master Password
    check_db_master_password = False
    while not check_db_master_password:
        print('\n' + tag + 'Database Master Password:', end=' ')
        db_master_password = input()
        if re.search(r'[^\/\"\@]{8,128}', db_master_password):
            check_db_master_password = True
            config['MasterUserPassword'] = db_master_password
        elif db_master_password.lower().startswith('!more'):
            print('\n' + tag + 'Database Master Password\n' + 'The password for the master user.\n' +
                    '\nConstraints:\n' +
                    '- Must be 8 to 128 ANSI characters (excluding \"/\", \'"\', \"@\")')
        else:
            print(Style.BRIGHT + 'Invalid entry. Type ' + Fore.YELLOW + '!more' + Fore.RESET + ' for more information.')
   
    # Configuration Confirmation
    print('\n' + tag + 'Configuration Confirmation')
    print(Style.BRIGHT + '- RDS Instance Name: ' + Fore.CYAN + rds_name + Fore.RESET)
    print(Style.BRIGHT + '- Database Name: ' + Fore.CYAN + db_name + Fore.RESET)
    print(Style.BRIGHT + '- Database Engine: ' + Fore.CYAN + db_engine + Fore.RESET)
    print(Style.BRIGHT + '- Database Port: ' + Fore.CYAN + db_port + Fore.RESET)
    print(Style.BRIGHT + '- Database Instance Class: ' + Fore.CYAN + db_class + Fore.RESET)
    print(Style.BRIGHT + '- Database Storage Type: ' + Fore.CYAN + db_storage_type + Fore.RESET)
    print(Style.BRIGHT + '- Database Storage Size: ' + Fore.CYAN + db_storage_size + ' GiB' + Fore.RESET)
    if db_storage_type == 'io1':
        print(Style.BRIGHT + '- IOPS Value: ' + Fore.CYAN + iops_value + Fore.RESET)
    else:
        config['Iops'] = 0
    print(Style.BRIGHT + '- Database Master Username: ' + Fore.CYAN + db_master_username + Fore.RESET)
    print(Style.BRIGHT + '- Database Master Password: ' + Fore.CYAN + db_master_password + Fore.RESET)
    check_confirm_config = False
    while not check_confirm_config:
        confirm_config = input('\nConfirm this configuration:' + options)
        if confirm_config.lower().startswith('y'):
            check_confirm_config = True
            cri.create_rds_instance('', **config)
        elif confirm_config.lower().startswith('n'):
            print('\n' + tag + 'Cancelled.' + Fore.RED + '\nExiting program:' + Fore.RESET + ' You have chosen to cancel the configuration.')
            sys.exit(0)
        elif confirm_config.lower().startswith('!more'):
            print(tag + 'Configuration Confirmation\n' + 'If you choose to confirm the configuration (\'y\'), the RDS instance will be created with these values.\n' +
                    'If you choose to cancel the configuration (\'n\'), the program will exit and you must start over.')
        else:
            print(tag + 'Invalid entry. Type ' + Fore.YELLOW + '!more' + Fore.RESET + ' for more information.')