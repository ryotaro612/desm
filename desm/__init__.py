"""https://www.microsoft.com/en-us/research/project/dual-embedding-space-model-desm/?from=http%3A%2F%2Fresearch.microsoft.com%2Fprojects%2Fdesm#!downloads
"""
import click


class DogeType(click.ParamType):

    def convert(self, value, param, ctx):
        print(value)
        return str(value)
        

@click.command()
@click.option('--count', default=1, help='Number of greetings.', type=DogeType())
def cli(count):
    pass

def main():
    cli()
