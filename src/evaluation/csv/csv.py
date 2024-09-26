from fandango.language.parse import parse_file


def main():
    grammar, constraint, _ = parse_file("csv.fan")

    print("Grammar:", grammar)
    print("Constraint:", constraint)

if __name__ == "__main__":
    main()