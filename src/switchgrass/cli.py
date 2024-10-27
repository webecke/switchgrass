import sys
from typing import Dict, Callable


def default_quit_handler(cli: "CLI"):
    try:
        confirm = cli.get_input_bool("Are you sure you want to quit?")
        if confirm:
            sys.exit(0)
        else:
            print("Canceling quit")
            return
    except UserCancel:
        print("Canceling quit")
        return


class CLI:
    def __init__(self,
                 program_name: str = "program",
                 input_indicator: str = "> ",
                 cancel_message: str = "Input canceled"):
        self.name: str = program_name
        self._steps: Dict[str, Step] = {}
        self._input_indicator = input_indicator
        self._cancel_message = cancel_message
        self._quit_handler = default_quit_handler

    """============
    Step Management
    ============"""

    def add(self, step_name: str, handler: Callable[["CLI"], any]):
        self._steps[step_name] = Step(step_name, handler)

    def goto(self, step_name):
        if step_name not in self._steps.keys():
            raise InvalidStepError(f"Step '{step_name}' does not exist")
        return self._steps[step_name].handler(self)

    def run(self, starting_step: str):
        self.goto(starting_step)

    def goto_quit(self):
        self._quit_handler(self)

    """=======
    User Input
    ======="""

    def get_input(self, prompt: str = None) -> str:
        if prompt is not None:
            print(prompt)

        try:
            return input(self._input_indicator).strip()
        except KeyboardInterrupt:
            print(f"\n{self._cancel_message}")
            raise UserCancel
        except EOFError:
            print()  # ensures there's a blank line for the quit handler to start on
            self.goto_quit()

    def get_input_bool(self, prompt: str = None) -> bool:
        while True:
            response = self.get_input(prompt).lower()
            match response:
                case "yes" | "y":
                    return True
                case "no" | "n":
                    return False
                case _:
                    print("Please enter 'yes' or 'no' (or 'y'/'n')")

    def get_input_int(self, prompt: str = None, type_name: str = "integer") -> int:
        while True:
            try:
                return int(self.get_input(prompt))
            except ValueError:
                print(f"Must be a valid {type_name}")

    def get_input_float(self, prompt: str, type_name: str = "number") -> float:
        while True:
            try:
                return float(self.get_input(prompt))
            except ValueError:
                print(f"Must be a valid {type_name}")


class Step:
    def __init__(self, step_name: str, handler: Callable):
        self.name: str = step_name
        self.handler: Callable = handler


"""
CLI Errors
"""


class CLIError(Exception):
    """Base class for CLI errors"""
    pass


class InvalidStepError(CLIError):
    pass


class UserCancel(CLIError):
    pass


class ProgramExit(CLIError):
    pass
