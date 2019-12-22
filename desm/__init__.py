"""Expose the entrypoint."""
import click
import gensim.models.word2vec as w
from greentea.log import LogConfiguration
from .word2vec import Word2VecFactory
from .model_location import ModelLocation
from .model import DesmInOut, Desm
from .keyword import KeywordContext
from .similarity_request import SimilarityRequest
from .gateway.similarity import SimilarityGateway
from .service.similarity import SimilarityService


@click.group()
@click.option('-v', '--verbose', is_flag=True)
def main(verbose):
    """Illustrate usage of DESM."""
    LogConfiguration(verbose, 'desm').configure()


@main.command()
@click.option('--min-count', type=int, required=False)
@click.argument('corpus', type=w.LineSentence)
@click.argument('destination', type=ModelLocation.create)
def train(corpus, destination, **kwargs):
    """Train a word2vec model.

    CORPUS: A text file that each line is a setence.

    DESTINATION: Path to a file to save the trained model.

    """
    word2vec = Word2VecFactory.create(**kwargs)

    word2vec.build_vocab(corpus)

    word2vec.train(sentences=corpus,
                   total_examples=word2vec.corpus_count,
                   epochs=word2vec.epochs)
    with destination.open_writable_stream() as stream:
        word2vec.save(stream)


@main.group()
def build():
    """Create a DESM model."""


@build.command()
@click.argument('word2vec', type=ModelLocation.create)
@click.argument('desm', type=ModelLocation.create)
def inout(word2vec, desm):
    """Create a IN-OUT model.

    WORD2VEC    Path to a trained word2vec model.

    """
    with word2vec.get_filepath() as filepath:
        trained_word2vec = w.Word2Vec.load(filepath)
    DesmInOut(trained_word2vec).save(desm)


@main.command()
@click.option('--top-n', type=int, default=10)
@click.argument('desm', type=ModelLocation.create)
@click.argument('keywords', type=KeywordContext)
@click.argument('output', type=SimilarityGateway)
def similarity(
        top_n,
        desm: ModelLocation,
        keywords: KeywordContext,
        output):
    """Find the top-N most similar words.

    KEYWORDS:

    OUTPUT:

    """
    model = Desm.load(desm)
    service = SimilarityService(model, output)
    request = SimilarityRequest(top_n, keywords)
    service.find_similar_keywords(request)
