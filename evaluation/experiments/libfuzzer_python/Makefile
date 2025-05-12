.PHONY: all

all: clean harness_arg harness_stdin harness_file harness_libfuzzer harness_shared

COMPILE = clang -g -O2 -fsanitize=fuzzer-no-link
FANDANGO_BASE = fandango --verbose fuzz -n 1000 -f dummy.fan --file-mode=binary

harness_arg: example_harness.c
	$(COMPILE) \
		-o example_harness_arg example_harness.c

harness_stdin: example_harness.c
	$(COMPILE) \
		-DINPUT_STDIN \
		-o example_harness_stdin example_harness.c

harness_file: example_harness.c
	$(COMPILE) \
		-DINPUT_FILE \
		-o example_harness_file	 example_harness.c

harness_libfuzzer: example_harness.c libafl_libfuzzer
	$(COMPILE) \
		-L./LibAFL/libafl_libfuzzer_runtime \
		-Wl,-rpath,@loader_path \
		-lafl_libfuzzer_runtime \
		-DLIBFUZZER_MAIN \
		-o example_harness_libfuzzer example_harness.c

harness_shared: example_harness.c
	$(COMPILE) -shared -o example_harness_shared.dylib example_harness.c

LibAFL/.git:
	git clone https://github.com/AFLplusplus/LibAFL.git

libafl_libfuzzer: LibAFL/.git
	cd LibAFL/libafl_libfuzzer_runtime && ./build.sh
	cp LibAFL/libafl_libfuzzer_runtime/libafl_libfuzzer_runtime.dylib .

run_fandango_stdin: harness_stdin
	$(FANDANGO_BASE) --input-method stdin ./example_harness_stdin

run_fandango_file: harness_file
	$(FANDANGO_BASE) --input-method filename ./example_harness_file

run_fandango_libfuzzer: harness_shared
	$(FANDANGO_BASE) --input-method libfuzzer ./example_harness_shared.dylib

clean:
	rm -rf example_harness_*
