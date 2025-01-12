## local imports
from quiggle.cli.version import update_version
from quiggle.config.root import config_root
from quiggle.tools.printer import print_error, print_note

## global imports
import sys

class CliController:

	COMMANDS = {
		'updateversion': update_version
	}

	def __init__(self) -> None:
		self.args:    list = []
		self.command:  str = ''
		self.values:  list = []
		self.options: list = []
		self.flags:   list = []
		self._get_args()

	def _get_args(self) -> None:
		if len(sys.argv) < 2:
			return self._help_menu()
		self.args: list = sys.argv[1:]
		for arg in self.args: self._handle_parsing(arg)
		return self._parse_command()
        
	def _parse_command(self) -> None:
		if self.command in self.COMMANDS.keys():
			self.COMMANDS[self.command](self, config_root('globals'))
		else: print_error(f'Invalid command: "{ self.command }"')

	def _append_to_last_option(self, array: list, arg: any, key: str = None):
		last_option = array[-1]
		if key: last_option = last_option[key]
		last_option.append(arg)

	def _handle_parsing(self, arg: str) -> None:
		if arg == '-' or arg[0] != '-':
			if self.command == '': self.command = arg
			elif len(self.options) == 0: self.values.append(arg)
			else:	self._append_to_last_option(self.options, arg, 'values')
		elif arg[1] != '-':	self.flags.append(arg[1:])
		else:	self.options.append({	'option': arg[2:], 'values': [] })
	
	def filter_flags(self, flags: list):
		for flag in self.flags:
			if flag not in flags:
				print_note(f'Ignored -{ flag } flag.')
				self.flags.remove(flag)

	def filter_options(self, options: list):
		for option in self.options:
			if option['option'] not in options:
				print_note(f'Ignored --{ option['option'] } option.')
				self.options.remove(option)

	def _help_menu(self):
		print('Help Menu')