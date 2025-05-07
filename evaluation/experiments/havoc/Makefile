.PHONY: all get_coverage

all: get_coverage

giflib: giflib-code/.git
	cd giflib-code && make CFLAGS="-fprofile-arcs -ftest-coverage -fPIC" libgif.a

giflib-code/.git:
	git clone https://git.code.sf.net/p/giflib/code giflib-code

gif_parser: gif_parser.c giflib
	gcc -fprofile-arcs -ftest-coverage -I./giflib-code -o gif_parser gif_parser.c ./giflib-code/libgif.a

get_coverage: gif_parser
	# Havoc and branch mutation
	rm -f **/*.gcda
	fandango fuzz -f havoc_gif.fan -n 10000 --input-method=stdin --file-mode=binary  ./gif_parser
	gcovr -r . --txt-metric branch --txt --output branch_coverage_havoc.txt
	# Pure branch mutation
	rm -f **/*.gcda
	fandango fuzz -f havoc_gif.fan -n 10000 --input-method=stdin --file-mode=binary  ./gif_parser
	gcovr -r . --txt-metric branch --txt --output branch_coverage_pure.txt

clean:
	rm -f gif_parser
	rm -f **/*.gcno **/*.gcda **/*.gcov
	rm -f branch_coverage_havoc.txt branch_coverage_pure.txt
	cd giflib-code && make clean