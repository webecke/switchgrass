from src.switchgrass.cli import CLI


def start_up(cli: CLI):
    print("Welcome to the Example Calculator!")
    print("Powered by switchgrass 🌾")

    cli.go_to("main")

    print("I guess we're done here")


def main_menu(cli: CLI):
    thing_to_do = input("What do you want to do?\n")

    cli.go_to(thing_to_do)


def add_menu(cli: CLI):
    num1 = float(input("number 1: "))
    num2 = float(input("number 2: "))
    sum = num1 + num2
    print(f"{num1} + {num2} = {sum}")
    return sum


if __name__ == "__main__":
    cli = CLI("Example Calculator")

    cli.add("start", start_up)
    cli.add("main", main_menu)
    cli.add("add", add_menu)

    cli.run("start")
