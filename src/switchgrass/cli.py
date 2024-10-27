import sys
from typing import Dict, Callable


def default_quit_handler(cli: "CLI"):
    try:
        confirm = cli.get_input_bool("Are you sure you want to quit?")
        if confirm:
            print("Ok, goodbye")
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
                 cancel_message: str = "Input canceled",
                 input_true_options: set[str] = None,
                 input_false_options: set[str] = None,
                 input_bool_error_message: set[str] = "Please enter 'yes' or 'no' (or 'y'/'n')",
                 cancel_commands: set[str] = None,
                 quit_commands: set[str] = None):
        self.name: str = program_name
        self._steps: Dict[str, Step] = {}
        self._global_commands: Dict[str, Callable[["CLI"], None]] = {}

        # input management strings
        self._input_indicator = input_indicator
        self._input_true_options = {option.lower() for option in (input_true_options or {"yes", "y"})}
        self._input_false_options = {option.lower() for option in (input_false_options or {"no", "n"})}
        self._input_bool_error_message = input_bool_error_message

        # control-flow options
        self._cancel_message = cancel_message
        self._quit_handler = default_quit_handler
        self._cancel_commands = {cmd.lower() for cmd in (cancel_commands or {"cancel"})}
        self._quit_commands = {cmd.lower() for cmd in (quit_commands or {"quit", "exit"})}

    """============
    Step Management
    ============"""

    def add(self, step_name: str, handler: Callable[["CLI"], any]):
        self._steps[step_name] = Step(step_name, handler)

    def add_global_command(self, command: str, handler: Callable[["CLI"], None]):
        self._global_commands[command] = handler

    def add_quit(self, handler: Callable[["CLI"], None]):
        self._quit_handler = handler

    def goto(self, step_name: str):
        if step_name not in self._steps.keys():
            raise InvalidStepError(f"Step '{step_name}' does not exist")
        return self._steps[step_name].handler(self)

    def goto_global(self, command: str):
        if command not in self._global_commands.keys():
            raise InvalidStepError(f"Global command '{command}' does not exist")
        return self._global_commands[command](self)

    def run(self, starting_step: str):
        self.goto(starting_step)

    def goto_quit(self):
        return self._quit_handler(self)

    """=======
    User Input
    ======="""

    def get_input(self, prompt: str = None) -> str:
        if prompt is not None:
            print(prompt)

        try:
            response: str = input(self._input_indicator).strip()

            match response.lower():
                case command if command in self._quit_commands:
                    raise EOFError
                case command if command in self._cancel_commands:
                    raise KeyboardInterrupt
                case command if command in self._global_commands.keys():
                    self.goto_global(command)
                    return self.get_input(prompt)

            return response

        except KeyboardInterrupt:
            print(f"\n{self._cancel_message}")
            raise UserCancel
        except EOFError:
            print()  # ensures there's a blank line for the quit handler to start on
            self.goto_quit()
            return self.get_input(prompt)  # if the quit handler decides not to quit, reprompt for input right where you left off

    def get_input_bool(self, prompt: str = None) -> bool:
        while True:
            response = self.get_input(prompt).lower()
            match response.lower():
                case option if option in self._input_true_options:
                    return True
                case option if option in self._input_false_options:
                    return False
                case _:
                    print(self._input_bool_error_message)

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
