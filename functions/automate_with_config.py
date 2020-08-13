import json
from colorama import init, Fore, Back, Style
from functions import create_rds_instance as cri
init(convert=True)

# Tag & Options
tag = Style.BRIGHT + Fore.BLUE + '[fast-rds] ' + Fore.RESET

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

def automate_with_config(auto_name):

    with open('./configs/' + auto_name + '.json', "r") as read_file:
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
                #print(Fore.YELLOW + key[0] + ' skipped as empty')
                del config[key[0]]
    
    cri.create_rds_instance(auto_name, **config)