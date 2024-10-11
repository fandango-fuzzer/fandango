from fandango.language.parse import parse_file


def main():
    # Load the fandango file
    grammar, constraints = parse_file("demo.fan")

    print("Grammar:")
    print(grammar)

    print("Constraints:")
    print(constraints)

if __name__ == "__main__":
    main()