from typing import Dict, Callable


class CLI:
    def __init__(self, program_name: str = "program"):
        self.name: str = program_name
        self._steps: Dict[str, Step] = {}

    def add(self, step_name: str, handler: Callable[["CLI"], any]):
        self._steps[step_name] = Step(step_name, handler)

    def go_to(self, step_name):
        return self._steps[step_name].handler(self)

    def run(self, starting_step: str):
        print("Starting...")
        self._steps[starting_step].handler(self)


class Step:
    def __init__(self, step_name: str, handler: Callable):
        self.name: str = step_name
        self.handler: Callable = handler
