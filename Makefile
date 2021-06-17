.PHONY: clean clean-test clean-pyc clean-build docs help

docs: ## generate Sphinx HTML documentation, including API docs
	rm -f docs/transkribus2arche.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ transkribus2arche */migrations/*
	$(MAKE) -C docs clean
	$(MAKE) -C docs html