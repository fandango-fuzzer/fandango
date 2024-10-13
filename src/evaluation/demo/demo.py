import time

from fandango.language.parse import parse_file


def main():
    # Load the fandango file
    grammar, constraints = parse_file("demo.fan")

    start_time = time.time()
    for _ in range(1000):
        solution = grammar.fuzz()
        # print(solution)

    print("Time taken: ", time.time() - start_time)

if __name__ == "__main__":
    main()