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

# automate_with_config(str):
# reads a json file with the provided auto_name
# from the ./configs/ directory and calls
# create_rds_instance() with the config dict.
def automate_with_config(auto_name):

    # Open ./configs/"auto_name".json
    with open('./configs/' + auto_name + '.json', "r") as read_file:
        config_file = json.load(read_file)

        # Iterate over keys in config
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
                #print(Fore.YELLOW + key[0] + ' skipped as empty')  # Warning for skipped configuration lines
                del config[key[0]]
    
    # Create RDS instance with resulting config dict
    cri.create_rds_instance(auto_name, **config)