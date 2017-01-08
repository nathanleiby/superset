SHELL := /bin/bash
.PHONY: test deps lint format

deps:
	pip install -r requirements-dev.txt

# Check for errors in Python files
pylint: deps
	find . | grep .py$$ | xargs pylint -E

lint: deps
	pep8 --config ./pep8 . || true

format: deps
	autopep8 -i -r -j0 -a --experimental .

# nose test-runner
nose:
	nosetests .

test: deps pylint nose

run:
	python main.py
	python vision.py
