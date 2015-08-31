import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "experiments",
    version = "0.0.1",
    author = "Hélain Schoonjans",
    author_email = "helain90@hotmail.com",
    description = ("Some statistical experiments on Facebook."),
    license = "MIT license",
    keywords = "facebook statistics",
    #url = "http://packages.python.org/an_example_pypi_project",
    packages=['facebook-sdk'],
    long_description=read('README.md'),
    #classifiers=[
    #    "Development Status :: 3 - Alpha",
    #    "Topic :: Utilities",
    #    "License :: OSI Approved :: BSD License",
    #],
) 