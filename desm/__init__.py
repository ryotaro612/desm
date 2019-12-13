"""Expose the entrypoint."""
import click
from greentea.log import LogConfiguration
from .corpus import Corpus


@click.group()
@click.option('-v', '--verbose', is_flag=True)
def main(verbose):
    """Illustrate usage of DESM."""
    LogConfiguration(verbose, 'desm').configure()


@main.command()
@click.option('--size', type=int)
@click.argument('corpus', type=Corpus.create_from_file)
def train(corpus):
    """Train a word2vec model.

    CORPUS: A text file that each line is a setence.

    """
    print('doge')
