# DESM
An implementation of a [Dual Embedding Space Model for Document Ranking(DESM)](https://arxiv.org/pdf/1602.01137.pdf).

[A gentile introduction to DESM](https://nryotaro.dev/posts/a_dual_embedding_space_model_for_document_ranking/).

## Build status
[![CircleCI](https://circleci.com/gh/nryotaro/desm.svg?style=svg)](https://circleci.com/gh/nryotaro/desm)

## Usage
`./tests/test_main.py` exposes a common use case.

## Documents
- [0.0.1](https://nryotaro.dev/desm/0.0.1/)

## Develpoment
[`Makefile`](./Makefile) provides build automation utilities, and `help` target displays its usage.

### Prerequisites
- Python (required versions are specified in [`setup.py`](./setup.py))
- make

### Tests
[`Makefile`](./Makefile) provides the target that runs unit tests.

    make test
