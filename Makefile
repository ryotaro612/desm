PACKAGE_NAME := desm
BASE_DIR := $(dir $(lastword $(MAKEFILE_LIST)))
PYENV_FILE := $(BASE_DIR).python-version
PYTHON_VERSION ?= 3.8.0
TEST_VENV ?= $(BASE_DIR).test_venv/
DOC_BUILD_DIR ?= $(BASE_DIR).doc_build/
DOC_VENV ?= $(BASE_DIR).doc_venv/
DOC_DIR ?= $(BASE_DIR)doc/

help: ## Display this help.
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n\nTargets:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

test: $(TEST_VENV)bin/pytest ## Run tests.
	cd $(BASE_DIR) && \
	. $(TEST_VENV)bin/activate && \
	pytest

doc: $(DOC_VENV)bin/sphinx-build $(DOC_BUILD_DIR)conf.py $(DOC_BUILD_DIR)index.rst ## Generate docs.
	. $(DOC_VENV)bin/activate && \
	sphinx-apidoc -M -f -o $(DOC_BUILD_DIR) $(PACKAGE_NAME) && \
	sphinx-build -a $(DOC_BUILD_DIR) $(DOC_DIR)

clean: clean_test clean_doc ## Delete unnecessary files.

clean_test: ## Delete the unnecessary resources for running test.
	rm -rf $(TEST_VENV) $(BASE_DIR).pytest_cache

clean_doc: ## Delete the unnecessary resources for generating documents.
	rm -rf $(DOC_BUILD_DIR) $(DOC_VENV) $(DOC_DIR)

$(TEST_VENV)bin/pytest: $(PYENV_FILE)
	cd $(BASE_DIR) && \
	python -m venv $(TEST_VENV) && \
	. $(TEST_VENV)bin/activate && \
	pip install --upgrade pip && \
	pip install -e .[test]

$(DOC_BUILD_DIR)conf.py:
	cd $(BASE_DIR) && \
	mkdir -p $(DOC_BUILD_DIR) && \
	cp config/conf.py $(DOC_BUILD_DIR)conf.py

$(DOC_BUILD_DIR)index.rst:
	cd $(BASE_DIR) && \
	mkdir -p $(DOC_BUILD_DIR) && \
	cp config/index.rst $(DOC_BUILD_DIR)index.rst

$(DOC_VENV)bin/sphinx-build: $(PYENV_FILE)
	cd $(BASE_DIR) && \
	python -m venv $(DOC_VENV) && \
	. $(DOC_VENV)bin/activate && \
	pip install --upgrade pip && \
	pip install -e .[doc]

$(PYENV_FILE): 
	cd $(BASE_DIR) && \
	pyenv local $(PYTHON_VERSION)

.PHONY: help clean clean_test clean_doc doc

