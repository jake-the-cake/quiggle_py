## global imports
import sys

class CliController:

    def __init__(self) -> None:
        self.command:  str = ''
        self.args:    list = []
        self.values:  list = []
        self.options: list = []
        self.flags:   list = []
        self._get_args()
        self._parse_command()
        print(vars(self))

    def _get_args(self):
        if len(sys.argv) < 2:
            return self._help_menu()
        self.args:    list = sys.argv[1:]

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
                    'flag': arg,
                    'values': [] 
                })

    def _help_menu(self):
        print('Help Menu')

    # def _ne

def update_version(path: str) -> None:
    cli = CliController()
    variable = 'VERSION_NUMBER'
    with open(path) as file:
        lines = file.readlines()
    updated_lines = []
    for line in lines:
        print(line)
        if line[:len(variable)] == variable:
            split_line = line.replace(' ', '').replace('\n', '').split('=')
            version_parts = split_line[1].replace('\'', '').split('.')
            if len(cli.values) > 0:
                split_line[1] = '\'' + cli.values[0] + '\'\n'
            else:
                split_line[1] = '.'.join(split_line[1])
            updated_lines.append(' = '.join(split_line))
        else: updated_lines.append(line)
    print(updated_lines)