install:
	pip install .

test:
	pytest

evaluation:
	python evaluation/vs_isla/run_evaluation.py