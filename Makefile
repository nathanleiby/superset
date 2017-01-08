SHELL := /bin/bash
.PHONY: test deps lint format

deps:
	pip install -q -r requirements-dev.txt

lint: deps
	flake8

format: deps
	autopep8 -i -r -j0 -a --experimental .

# nose test-runner
nose: deps
	nosetests .

test: deps lint nose

run: deps
	python game.py
	python vision.py
