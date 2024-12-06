## global imports
import sys

class CliController:

    def __init__(self) -> None:
        if len(sys.argv) < 2: raise Exception('No command given.')
        self.args = sys.argv[1:]


def update_version():
    cli = CliController()
    print(cli.args)