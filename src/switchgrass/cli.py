from typing import Dict, Callable


class CLI:
    def __init__(self,
                 program_name: str = "program",
                 input_indicator: str = "> "):
        self.name: str = program_name
        self._steps: Dict[str, Step] = {}
        self._input_indicator = input_indicator

    """============
    Step Management
    ============"""

    def add(self, step_name: str, handler: Callable[["CLI"], any]):
        self._steps[step_name] = Step(step_name, handler)

    def go_to(self, step_name):
        return self._steps[step_name].handler(self)

    def run(self, starting_step: str):
        print("Starting...")
        self._steps[starting_step].handler(self)

    """=======
    User Input
    ======="""

    def get_input(self, prompt: str) -> str:
        print(prompt)
        return input(self._input_indicator).strip()

    def get_input_bool(self, prompt: str) -> bool:
        while True:
            response = self.get_input(prompt).lower()
            match response:
                case "yes" | "y":
                    return True
                case "no" | "n":
                    return False
                case _:
                    print("Please enter 'yes' or 'no' (or 'y'/'n')")

    def get_input_int(self, prompt: str, type_name: str = "integer") -> int:
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
