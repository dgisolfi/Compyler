# Compyler
# Author:  Daniel Nicolas Gisolfi

repo=Compyler
version=0.4.2

release: clean intro build publish

intro:
	@echo "\n $(repo) v$(version)"

init:
	@echo "\nInstalling all requirements found in requirements.txt"
	@python3 -m pip install -r requirements.txt

clean:
	-rm -r ./build
	-rm -r ./dist
	-rm -r ./$(repo).egg-info

build:
	@python setup.py sdist

publish:
	@python3 -m twine upload dist/*

install:
	@python3 -m pip install .

uninstall:
	@python3 -m pip uninstall $(repo)==$(version)

.PHONY: init clean test build
