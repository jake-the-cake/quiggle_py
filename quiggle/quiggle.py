## local imports
from quiggle.docs import doc
from quiggle.config.globals import VERSION_NUMBER
from quiggle.tools.logs.colors import Colors
from quiggle.tools.logs.presets import errorlog, questionlog
from quiggle.prompts import MAIN_MENU, MESSAGES

## gloabal imports
import os
from pathlib import Path

## documentation
DOC = doc(
	'Quiggle Application',
	usage = '''
	text()
	'''
)

def welcome_screen() -> None:
	print(MESSAGES['welcome'])

def main_prompt() -> None:
	answer = input(MAIN_MENU)

	valid_answers = {
		'1': create,
		'2': create,
		'3': create
	}

	if answer in valid_answers.keys():
		valid_answers[answer]()
	else:
		print(ValueError(errorlog('Invalid option.')))
		main_prompt()

################
''' # create '''
# create a new project with default pages
def create():
	DOC.function(create.__name__, '')
	
	print(Colors.YELLOW + '\nSETUP' + Colors.RESET)
	def ask_for_project_name():
		name       = input(questionlog('What is the project name? '))
		valid_name = name.strip().lower().replace(' ', '-')
		#
		''' # strip special chars '''
		#
		

		if not name == valid_name:
			
			# print(Colors.BRIGHT_CYAN + 'A change was made to your project name' + Colors.RESET)
			print(MESSAGES['project_name_change'])
			agree = input('Use name "{}"? [y/n] '.format(valid_name))
			
			if not agree == 'y' and not agree == '':
				print('Ok then, let\'s try that again.')
				return ask_for_project_name()
		
		if os.path.isdir(os.path.join(os.getcwd(), name)):
			print(Exception(errorlog("Project name exists.")))
			return ask_for_project_name()
		return valid_name

	name        = ask_for_project_name()
	root_dir    = os.getcwd()
	setup_dir   = os.path.join(Path(__file__).parent, 'setup')
	project_dir = os.path.join(root_dir, name)

	# create project directory
	os.makedirs(project_dir, exist_ok=True)

	# define the folder structure
	STRUCTURE = {
		'config': [],
		'public': [{
			'css': ['quiggle.css'],
			'js': ['quiggle.js'],
			'img': [],
		}],
		'templates': ['index.html'],
		'models': [],
		'router': [{'contact': ['view.py', 'api.py']}, 'view.py', 'api.py'],
		'__main__': ['app.py', 'config.py']
	}

	# add folders and files
	for key in STRUCTURE.keys():
		current_dir = project_dir

		if not key == '__main__':
			current_dir = os.path.join(project_dir, key)
			os.makedirs(current_dir, exist_ok=True)
		
		def build_file_system(arr, working_dir):	
			for item in arr:
				if isinstance(item, str):
					setup_file = os.path.join(setup_dir, item)
					file_path  = os.path.join(working_dir, item)
					
					with open(file_path, 'w') as dest:
						if os.path.exists(setup_file):
							with open(setup_file, 'r') as src:
								content = src.read()
								dest.write(content)
						else:
							dest.write('# auto-generated by quiggle')

				else:
					for k in item.keys():
						new_dir = os.path.join(working_dir, k)
						os.makedirs(new_dir)
						build_file_system(item[k], new_dir)
		
		build_file_system(STRUCTURE[key], current_dir)
	print(Colors.YELLOW + 'Setup complete for project "{}"'.format(name) + Colors.RESET)


##############
''' # main '''
# direct access to the main menu
def main() -> None:
	welcome_screen()
	main_prompt()

''' # run from direct file load '''
if __name__ == '__main__':	main()