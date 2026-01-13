CC = fcc

all:
	@mkdir -p build
	$(CC) -o build/test_malloc_calloc src/test_malloc_calloc.c
	$(CC) -o build/test_input_dependent_malloc src/test_input_dependent_malloc.c

clean:
	rm -rf build
	rm -rf .*.o.bc
	rm -rf .*.o