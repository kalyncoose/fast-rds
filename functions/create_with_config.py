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

def create_with_config(config_name):
    print('\n' + tag + 'Create With Config File\n' + 'Loading file: ' + config_name + '.json...')

    with open('./configs/' + config_name + '.json', "r") as read_file:
        config_file = json.load(read_file)
        for key in config_file.items():
            if key[0] in config_file and str(key[1]) != '':
                if key[0] == 'Tags' or key[0] == 'ProcessorFeatures':
                    keys = []
                    for i in key[1]:
                        keys.append(i[0].copy())
                    config[key[0]] = keys.copy()
                else:
                    config[key[0]] = key[1]
            else:
                print(Fore.YELLOW + key[0] + ' skipped as empty')
                del config[key[0]]

    # Configuration Confirmation
    print('\n' + tag + 'Configuration Confirmation')
    for key, value in config.items():
        if key == 'AllocatedStorage' or key == 'MaxAllocatedStorage':
            print(Style.BRIGHT + key + ': ' + Fore.CYAN + str(value) + ' GiB' + Fore.RESET)
        else:
            print(Style.BRIGHT + key + ': ' + Fore.CYAN + str(value) + Fore.RESET)
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