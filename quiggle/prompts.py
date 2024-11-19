from quiggle.tools.logs.presets import infolog
from quiggle.tools.logs.colors import Colors

from quiggle.config.globals import VERSION_NUMBER

MESSAGES = {
	'welcome': '\nQuiggle Web Framework by PBJ (version {})'.format(VERSION_NUMBER),
	'project_name_change': infolog('A change was made to your project name'),
}

##
''' # ADD FEATURE: Determine if project exists ''' 
NUM_3 = 'User'
##

MAIN_MENU = '''
	{}MAIN MENU{}
	1. Create New Project
	2. Add New Feature
	3. {}

What would you like to do? '''.format(Colors.YELLOW ,Colors.RESET, NUM_3)