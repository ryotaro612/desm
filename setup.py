"""
"""
from setuptools import setup, find_packages


setup(name='desm',
      version="0.0.1",
      description=(
          'TODO'),
      python_requires='>=3.8.0',
      url='https://github.com/nryotaro/desm',
      author='Nakamura, Ryotaro',
      author_email='nakamura.ryotaro.kzs@gmail.com',
      license='MIT License',
      classifiers=['Programming Language :: Python :: 3.8'],
      packages=find_packages(),
      install_requires=[
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
