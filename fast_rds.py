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

import sys
from colorama import init, Fore, Back, Style
from functions import create_with_config  as cwc
from functions import create_without_config as cwoc
from functions import automate_with_config as awc
init(convert=True)

# Tag & Options
tag = Style.BRIGHT + Fore.BLUE + '[fast-rds] ' + Fore.RESET
options = Style.BRIGHT + Fore.GREEN + ' [y]' + Fore.RED + '[n]' + Fore.YELLOW + '[!more]' + Fore.RESET + ': '

# Argument: None
if len(sys.argv) == 1:
    print(Style.BRIGHT + Fore.RED + 'Exiting program: ' + Fore.RESET + 
        'No supplied commands. Use ' + Fore.YELLOW + '\"!create\"' + Fore.RESET + ' or ' + Fore.YELLOW + '\"!help\"')
    sys.exit(0)

# Argument: !create
if sys.argv[1] == '!create':
    print(tag + 'Welcome to fast-rds!')

    check_config = False
    while not check_config:
        print('Do you want to use a configuration file?' + options, end=' ')
        use_config = input()

        if use_config.lower().startswith('y'):
            check_config = True
            check_name = False
            while not check_name:
                print('Please specify the config filename (excluding .json):', end=' ')
                config_name = input()
                if config_name != '' and not config_name.endswith('.json'):
                    check_name = True
                    cwc.create_with_config(config_name)
                else:
                    print(Style.BRIGHT + 'Invalid entry. Please enter a valid config filename exlcuding the ".json" extension.\n')
        elif use_config.lower().startswith('n'):
            check_config = True
            cwoc.create_without_config()
            
        elif use_config.lower().startswith('!more'):
            print('\n' + tag + 'Configuration Usage\n' + 'To use a config file, it must be of .json type and placed in ./configs directory.\n' +
                    'By default, an \"example.json\" is provided. It includes all RDS parameters.\n' +
                    'Copy and rename the file, then modify the configuration to your needs.\n')
        else:
            print(Style.BRIGHT + 'Invalid entry. Type ' + Fore.YELLOW + '!more' + Fore.RESET + ' for more information.\n')

# Argument: !automate [option]
elif sys.argv[1] == '!automate':
    if len(sys.argv) == 3:
        print(tag + 'Automating creation with ' + sys.argv[2])
    else:
        print(Style.BRIGHT + Fore.RED + 'Exiting program: ' + Fore.RESET +
            'An option was not provided. Use ' + Fore.YELLOW + '\"!help\"' + Fore.RESET + ' for more information.')
        sys.exit(0)

    if sys.argv[2] != '' and not sys.argv[2].endswith('.json'):
        awc.automate_with_config(sys.argv[2])
    else:
        print(Style.BRIGHT + Fore.RED + 'Exiting program: ' + Fore.RESET + '\"' + sys.argv[2] +
            '\" is not a valid option. Use ' + Fore.YELLOW + '\"!help\"' + Fore.RESET + ' for more information.')
        sys.exit(0)

# Argument: Invalid argument
else:
    print(Style.BRIGHT + Fore.RED + 'Exiting program: ' + Fore.RESET + '\"' + sys.argv[1] +
            '\" is not a valid command. Use ' + Fore.YELLOW + '\"!create\"' + Fore.RESET + ' or ' + Fore.YELLOW + '\"!help\"')
    sys.exit(0)