#!/usr/bin/env python
from setuptools import setup, find_packages
from alchemytools import __version__
import os

BASE_PATH = os.path.dirname(__file__)


setup(
    name='Alchemytools',
    version=__version__,
    description='Alchemytools is a set of helpers to be used in any SQLAlchemy project',
    long_description=open(os.path.join(BASE_PATH, 'README.rst')).read(),
    author='Dalton Barreto',
    author_email='daltonmatos@gmail.com',
    url='https://github.com/daltonmatos/alchemytools',
    packages=find_packages(),
    install_requires=['SQLAlchemy >=0.7.8, <=1.2.15'],
    tests_require=['tox==3.5.3', 'mock==2.0.0'],
    classifiers=[
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Topic :: Software Development',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
