from switchgrass import *  # Instead of from src.switchgrass.cli import CLI


def start_up(cli: CLI):
    print("Welcome to the Example Calculator!")
    print("Powered by switchgrass 🌾")

    cli.goto("main")

    print("I guess we're done here")


def main_menu(cli: CLI):
    while True:
        try:
            thing_to_do = cli.get_input("What do you want to do?")

            cli.goto(thing_to_do)

        except UserCancel:
            print("Hey, you canceled that")
        except InvalidStepError:
            print("That's not a valid input")


def add_menu(cli: CLI):
    num1 = cli.get_input_int("Number 1")
    num2 = cli.get_input_int("Number 2")
    ready = cli.get_input_bool("Are you ready?")
    if not ready:
        print("oh, ok")
        return
    sum = num1 + num2
    print(f"{num1} + {num2} = {sum}")
    return sum


if __name__ == "__main__":
    cli = CLI("Example Calculator")

    cli.add("start", start_up)
    cli.add("main", main_menu)
    cli.add("add", add_menu)

    cli.run("start")
