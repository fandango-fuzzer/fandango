.PHONY: gif_parser libfuzzer 

FANDANGO_ITERATIONS=10000

giflib_gcov: giflib-code-gcov/.git
	cd giflib-code-gcov && make CFLAGS="-fprofile-arcs -ftest-coverage -fPIC" libgif.a

giflib-code-gcov/.git:
	git clone https://git.code.sf.net/p/giflib/code giflib-code-gcov

gif_parser: gif_parser.c giflib_gcov
	gcc -fprofile-arcs -ftest-coverage -I./giflib-code-gcov -o gif_parser gif_parser.c ./giflib-code-gcov/libgif.a

giflib_libfuzzer: giflib-code-libfuzzer/.git
	cd giflib-code-libfuzzer && make CFLAGS="-fsanitize=fuzzer-no-link,address" libgif.a

giflib-code-libfuzzer/.git:
	git clone https://git.code.sf.net/p/giflib/code giflib-code-libfuzzer

LibAFL/.git:
	git clone https://github.com/AFLplusplus/LibAFL.git

libafl_libfuzzer: LibAFL/.git
	cd LibAFL/libafl_libfuzzer_runtime && ./build.sh
	cp LibAFL/libafl_libfuzzer_runtime/libafl_libfuzzer_runtime.dylib .

libfuzzer: giflib_libfuzzer libafl_libfuzzer
	clang -O2 -g \
		-fsanitize=fuzzer-no-link,address  \
		-L./LibAFL/libafl_libfuzzer_runtime \
		-Wl,-rpath,@loader_path \
		-lafl_libfuzzer_runtime \
		-o libfuzzer_harness \
		./giflib-code-libfuzzer/libgif.a \
		harness_libfuzzer.c

run_libfuzzer: libfuzzer
	rm -rf corpus
	mkdir -p corpus
	cp tiny.gif corpus/
	./libfuzzer_harness corpus -fork=8 -ignore_ooms=1

post_libfuzzer:
	for file in corpus/*; do cat $$file | ./gif_parser; done

gcov: gif_parser
	@if [ -z "$(RUN_NAME)" ]; then \
		echo "Error: RUN_NAME variable is required. Usage: make gcov RUN_NAME=<filename>"; \
		exit 1; \
	fi
	cd giflib-code-gcov && gcov ./*.gcno -t > "../gcov_$(RUN_NAME).txt"
	gcov ./gif_parser-gif_parser.gcno -t >> "./gcov_$(RUN_NAME).txt"
	gcovr -r . --txt-metric branch --txt --output branch_coverage_$(RUN_NAME).txt

run_fandango: gif_parser
	@if [ -z "$(FAN_FILE)" ]; then \
		echo "Error: FAN_FILE variable is required. Usage: make run_fandango FAN_FILE=<filename>"; \
		exit 1; \
	fi
	@echo "Starting parallel fuzzing (Ctrl+C to stop)..."
	@bash -c '\
		trap "kill 0" SIGINT; \
		for i in {1..8}; do \
			while true; do \
				fandango --verbose fuzz -f $(FAN_FILE) -n $(FANDANGO_ITERATIONS) --input-method=stdin --file-mode=binary ./gif_parser; \
			done & \
		done; \
		wait'

clean_gcov:
	rm -f **/*.gcda **/*.gcno

clean: clean_gcov
	rm -f gif_parser
	rm -f libafl_libfuzzer_runtime.dylib
	rm -f libfuzzer_harness
	rm -rf libfuzzer_harness.dSYM
	rm -f harness-crashes.log
	if [ -d LibAFL ]; then cd LibAFL && cargo clean; fi
	if [ -d giflib-code-gcov ]; then cd giflib-code-gcov && make clean; fi
	if [ -d giflib-code-libfuzzer ]; then cd giflib-code-libfuzzer && make clean; fi