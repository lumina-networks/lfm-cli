.PHONY: release test docs dist

all:
	@echo "make test - run tox"
	@echo "make docs - build docs"
	@echo "make sdist - produce source distribution"

release: test docs sdist

test:
	pip install tox
	tox

docs:
	pip install sphinx sphinx-rtd-theme
	pandoc README.rst -f markdown -t rst -s -o docs/README.rst
	cd docs && make html

sdist:
	python setup.py sdist

wagon:
	rm -rf lfm-cli
	wagon create -f -r -s .

source_package:
	make clean; tar -zcvf ../lfm-cli.tar.gz --exclude='__MACOSX' --exclude='*.DS_Store'  --exclude='*.pyc' --exclude='.idea' --exclude='.git' --exclude='.env' --exclude='.venv' --exclude='*.tar.gz' -C .. ./lfm-cli

package:
	make source_package;