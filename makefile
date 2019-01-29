# Compyler
# Author:  Daniel Nicolas Gisolfi

repo=Compyler
version=0.0.1

release: clean intro test build publish

intro:
	@echo "\n $(repo) v$(version)"

init:
	@echo "\n Installing all requirements found in requirements.txt"
	@python3 -m pip install -r requirements.txt

clean:
	-rm -r ./build
	-rm -r ./dist
	-rm -r ./$(repo).egg-info

test: intro
	# @python3 -m pytest -s
	@python3 -m pytest

build:
	@python setup.py sdist

publish:
	@python3 -m twine upload dist/*

install:
	@python3 -m pip install .

uninstall:
	@python3 -m pip uninstall $(repo)

.PHONY: init clean test build
