from cli import CLI


def main_handler(cli: CLI):
    print("this is the main menu")
    thing = input("hey: ")
    print(thing)
    other = cli.go_to("other")
    print("This is what the other screen told me:")
    print(other)
    print("ok bye now")


def other_handler(cli: CLI):
    print("welcome to the other menu")
    another_thing = input("hey: ")
    return another_thing


if __name__ == "__main__":
    print("hey")
    cli = CLI("test_mcgee")

    cli.add("main", main_handler)
    cli.add("other", other_handler)

    cli.run("main")
