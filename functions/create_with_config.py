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

import json
import sys
from colorama import init, Fore, Back, Style
from functions import create_rds_instance as cri
init(convert=True)

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
    'DBSecurityGroups': '',
    'VpcSecurityGroupIds': '',
    'AvailabilityZone': '',
    'DBSubnetGroupName': '',
    'PreferredMaintenanceWindow': '',
    'DBParameterGroupName': '',
    'BackupRetentionPeriod': '',
    'PreferredBackupWindow': '',
    'Port': '',
    'MultiAZ': '',
    'EngineVersion': '',
    'AutoMinorVersionUpgrade': '',
    'LicenseModel': '',
    'Iops': '',
    'OptionGroupName': '',
    'CharacterSetName': '',
    'PubliclyAccessible': '',
    'Tags': '',
    'DBClusterIdentifier': '',
    'StorageType': '',
    'TdeCredentialArn': '',
    'TdeCredentialPassword': '',
    'StorageEncrypted': '',
    'KmsKeyId': '',
    'Domain': '',
    'CopyTagsToSnapshot': '',
    'MonitoringInterval': '',
    'MonitoringRoleArn': '',
    'DomainIAMRoleName': '',
    'Timezone': '',
    'EnableIAMDatabaseAuthentication': '',
    'EnablePerformanceInsights': '',
    'PerformanceInsightsKMSKeyId': '',
    'PerformanceInsightsRetentionPeriod': '',
    'EnableCloudwatchLogsExports': '',
    'DeletionProtection': '',
    'MaxAllocatedStorage': ''
}

# create_with_config(str):
# opens the ./configs/"config_name".json file
# and reads the config values to pass to
# create_rds_instance().
def create_with_config(config_name):
    print('\n' + tag + 'Create With Config File\n' + 'Loading file: ' + config_name + '.json...')

    # Open ./configs/"config_name".json file
    with open('./configs/' + config_name + '.json', "r") as read_file:
        config_file = json.load(read_file)
        
        # Iterate through keys in config
        for key in config_file.items():
            
            # Check if key's value is empty
            if key[0] in config_file and str(key[1]) != '':
                
                # Handle keys with list values
                if key[0] == 'Tags' or key[0] == 'ProcessorFeatures':
                    keys = []
                    for i in key[1]:
                        keys.append(i[0].copy())
                    config[key[0]] = keys.copy()
                
                # Handle keys with single values
                else:
                    config[key[0]] = key[1]
            
            # Delete unused config lines
            else:
                print(Fore.YELLOW + key[0] + ' skipped as empty')   # Warning for skipped configuration lines
                del config[key[0]]

    # Prompt user to confirm configuration values
    print('\n' + tag + 'Configuration Confirmation')
    
    # Iterate through values in config
    for key, value in config.items():
        
        # Handle GiB values
        if key == 'AllocatedStorage' or key == 'MaxAllocatedStorage':
            print(Style.BRIGHT + key + ': ' + Fore.CYAN + str(value) + ' GiB' + Fore.RESET)
        # Print config value
        else:
            print(Style.BRIGHT + key + ': ' + Fore.CYAN + str(value) + Fore.RESET)
    
    # Require user response to continue in instance creation
    check_confirm_config = False
    while not check_confirm_config:
        confirm_config = input('\nConfirm this configuration:' + options)
        
        # 'y' answer
        if confirm_config.lower().startswith('y'):
            check_confirm_config = True
            
            # Call create_rds_instance() with empty auto_name and include config dict
            cri.create_rds_instance('', **config)
        
        # 'n' answer
        elif confirm_config.lower().startswith('n'):
            print('\n' + tag + 'Cancelled.' + Fore.RED + '\nExiting program:' + Fore.RESET + ' You have chosen to cancel the configuration.')
            sys.exit(0)
        
        # '!more' answer
        elif confirm_config.lower().startswith('!more'):
            print(tag + 'Configuration Confirmation\n' + 'If you choose to confirm the configuration (\'y\'), the RDS instance will be created with these values.\n' +
                    'If you choose to cancel the configuration (\'n\'), the program will exit and you must start over.')
        
        # Invalid answer
        else:
            print(tag + 'Invalid entry. Type ' + Fore.YELLOW + '!more' + Fore.RESET + ' for more information.')