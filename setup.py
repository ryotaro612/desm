"""An implementation of dual embedding space model.

References
----------
https://www.microsoft.com/en-us/research/project/dual-embedding-space-model-desm/?from=http%3A%2F%2Fresearch.microsoft.com%2Fprojects%2Fdesm

"""
from setuptools import setup, find_packages


setup(name='desm',
      version="0.0.2",
      description=(
          'An implementation of dual embedding space model.'),
      python_requires='>=3.8.0',
      url='https://github.com/nryotaro/desm',
      author='Nakamura, Ryotaro',
      author_email='nakamura.ryotaro.kzs@gmail.com',
      license='MIT License',
      classifiers=['Programming Language :: Python :: 3.8'],
      packages=find_packages(),
      install_requires=[
          'joblib',
          'gensim',
          'click',
          'greentea==2.0.0'
      ],
      entry_points={'console_scripts': ['desm=desm:main']},
      extras_require={
          'test': [
              'pytest'
          ],
          'dev': [
              'ipython',
              'python-language-server[all]'
          ],
          'doc': [
              'sphinx',
              'sphinx_rtd_theme']})
