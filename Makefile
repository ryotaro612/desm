PACKAGE_NAME := desm
BASE_DIR := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))/
PYENV_FILE := $(BASE_DIR).python-version
PYTHON_VERSION ?= 3.8.0
VENV ?= $(BASE_DIR)venv/
BUILD_DIR ?= $(BASE_DIR).build/
DOC_BUILD_DIR ?= $(BASE_DIR).doc_build/
PROJECT_VERSION = $(shell cd $(BASE_DIR) && python -c "import ast; f = open('setup.py'); txt = ast.parse(f.read());f.close();print([keyword.value.value for node in txt.body if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call) and node.value.func.id == 'setup' for keyword in node.value.keywords if keyword.arg == 'version'][0]);")
DOC_DIR ?= $(BASE_DIR)docs/$(PROJECT_VERSION)/
REPOSITORY_URL := git@github.com:nryotaro/desm.git

help: ## Display this help.
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n\nTargets:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

publish: $(VENV)bin/activate $(BUILD_DIR)setup.py $(VENV)bin/twine  ## Clone codes in the revision tagged with 'TAG' to local, build them, then publish them to the pip index server.
	cd $(BUILD_DIR) && \
	git clean -fd && \
	rm -rf desm.egg-info dist build && \
	git checkout master && \
	git pull && \
	git checkout $(TAG) && \
	. $(VENV)bin/activate && \
	python setup.py sdist bdist_wheel && \
	python -m twine upload dist/*

test: $(VENV)bin/pytest ## Run tests.
	cd $(BASE_DIR) && \
	. $(VENV)bin/activate && \
	pytest

doc: $(BASE_DIR)docs/.nojekyll $(VENV)bin/sphinx-build $(DOC_BUILD_DIR)conf.py $(DOC_BUILD_DIR)index.rst ## Generate docs.
	. $(VENV)bin/activate && \
	sphinx-apidoc -M -f -o $(DOC_BUILD_DIR) $(PACKAGE_NAME) && \
	rm -rf $(DOC_DIR)* && \
	sphinx-build -a $(DOC_BUILD_DIR) $(DOC_DIR)
	rm -rf $(DOC_DIR).buildinfo $(DOC_DIR).doctrees $(DOC_BUILD_DIR)

clean: clean_test clean_doc ## Delete unnecessary files.
	rm -rf $(VENV)

clean_doc: ## Delete the unnecessary resources for doc target.
	rm -rf $(DOC_BUILD_DIR)

clean_test: ## Delete the unnecessary resources for test target.
	rm -rf $(BASE_DIR).pytest_cache

$(BUILD_DIR)setup.py:
	rm -rf $(BUILD_DIR)
	mkdir $(BUILD_DIR)
	git clone $(REPOSITORY_URL) $(BUILD_DIR)

$(VENV)bin/twine: $(VENV)bin/activate
	. $(VENV)bin/activate && \
	pip install --upgrade pip wheel twine

$(VENV)bin/pytest: $(VENV)bin/activate
	cd $(BASE_DIR) && \
	. $(VENV)bin/activate && \
	pip install --upgrade pip && \
	pip install -e .[test]

$(DOC_BUILD_DIR)conf.py:
	mkdir -p $(DOC_BUILD_DIR) && \
	cp $(BASE_DIR)config/conf.py $(DOC_BUILD_DIR)conf.py

$(DOC_BUILD_DIR)index.rst:
	mkdir -p $(DOC_BUILD_DIR) && \
	cp $(BASE_DIR)config/index.rst $(DOC_BUILD_DIR)index.rst

$(VENV)bin/sphinx-build: $(VENV)bin/activate
	cd $(BASE_DIR) && \
	. $(VENV)bin/activate && \
	pip install --upgrade pip && \
	pip install -e .[doc]

$(VENV)bin/activate: $(PYENV_FILE)
	cd $(BASE_DIR) && python -m venv $(VENV)

$(PYENV_FILE):
	cd $(BASE_DIR) && \
	pyenv local $(PYTHON_VERSION)

$(BASE_DIR)docs/.nojekyll:
	mkdir -p $(BASE_DIR)docs
	touch $(BASE_DIR)docs/.nojekyll

.PHONY: help doc clean clean_test  clean_doc
