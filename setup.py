import os
from setuptools import setup, find_packages

VERSION = "0.1.0.dev2"


# Read description
with open('README.rst', 'r') as readme:
    README_TEXT = readme.read()


def write_version_py():
    filename = os.path.join(
        os.path.dirname(__file__),
        'enthought_example',
        'version.py')
    ver = "__version__ = '{}'\n"
    with open(filename, 'w') as fh:
        fh.write(ver.format(VERSION))


write_version_py()

setup(
    name="enthought_example",
    version=VERSION,
    entry_points={
        "force.bdss.extensions": [
            "enthought_example = "
            "enthought_example.example_plugin:ExamplePlugin",
        ]
    },
    packages=find_packages(),
    install_requires=[
        "force_bdss >= 0.1.0.dev2",
    ]
)
