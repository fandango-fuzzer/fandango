CC = fcc

all:
	@mkdir -p build
	$(CC) -o build/test_simple src/test_simple.c
	$(CC) -o build/test_input_dependent src/test_input_dependent.c

clean:
	rm -rf build
	rm -rf .*.o.bc
	rm -rf .*.o