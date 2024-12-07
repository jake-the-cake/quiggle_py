## local imports
from quiggle.config import globals
from quiggle.tools.logs.presets import labellog

## global imports
import sys

def update_version(cli, path: str) -> None:
    cli._filter_flags(['minor', 'major'])
    variable = 'VERSION_NUMBER'
    with open(path, 'r') as file:
        lines = file.readlines()
    updated_lines = []
    for line in lines:
        if line[:len(variable)] == variable:
            split_line = line.replace(' ', '').replace('\n', '').split('=')
            original_value = split_line[1]
            if len(cli.values) > 0:
                split_line[1] = '\'' + cli.values[0] + '\'\n'
            elif len(cli.flags) > 0:
                for flag in cli.flags:
                    version_parts = split_line[1].replace('\'', '').split('.')
                    if flag['flag'] == 'minor':
                        version_parts[1] = str(int(version_parts[1]) + 1)
                        split_line[1] = '\'' + '.'.join(version_parts) + '\'\n'
            else:
                split_line[1] = '.'.join(split_line[1])
            updated_lines.append(' = '.join(split_line))
        else: updated_lines.append(line)
    print(''.join(updated_lines))

class CliController:

    COMMANDS = {
        'updateversion': update_version
    }

    def __init__(self) -> None:
        self.command:  str = ''
        self.args:    list = []
        self.values:  list = []
        self.options: list = []
        self.flags:   list = []
        self._get_args()
        self._parse_command()

    def _get_args(self):
        if len(sys.argv) < 2:
            return self._help_menu()
        self.args: list = sys.argv[1:]

    def _parse_command(self) -> None:
        for arg in self.args:
            if arg[0] != '-':
                if self.command == '':
                    self.command = arg
                elif len(self.flags) == 0:
                    self.values.append(arg)
                else:
                    self.flags[-1]['values'].append(arg)
            elif arg[1] != '-':
                self.options.append(arg[1:])
            else:
                self.flags.append({
                    'flag': arg[2:],
                    'values': [] 
                })
        if self.command in self.COMMANDS.keys():
            self.COMMANDS[self.command](self, globals.QUIGGLE_DIR + '/config/globals.py')
    
    def _filter_flags(self, flags: list):
        for flag in self.flags:
            if flag['flag'] not in flags:
                print(labellog(f'Ignored --{ flag['flag'] } flag.'))
                self.flags.remove(flag)

    def _help_menu(self):
        print('Help Menu')