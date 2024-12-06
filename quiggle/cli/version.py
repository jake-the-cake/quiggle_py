## global imports
import sys

class CliController:

    def __init__(self) -> None:
        if len(sys.argv) < 2: raise Exception('No command given.')
        self.args = sys.argv[1:]
        self.command = self.args[0]
        self.values = []
        self.flags = []
        self._parse_command()

    def _parse_command(self) -> None:
        if len(self.args) > 1:
            print(self.args[1:])

def update_version():
    cli = CliController()
    print(cli.args)