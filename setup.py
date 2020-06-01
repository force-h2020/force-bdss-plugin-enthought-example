#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

import os
from setuptools import setup, find_packages

VERSION = "0.4.0.dev"


# Read description
with open('README.rst', 'r') as readme:
    README_TEXT = readme.read()


def write_version_py():
    plugins = [
        'enthought_example',
        'eggbox_potential_sampler',
        'troughs_and_waves',
    ]
    for plugin in plugins:
        filename = os.path.join(
            os.path.dirname(__file__),
            plugin,
            'version.py')
        ver = "__version__ = '{}'\n"
        with open(filename, 'w') as fh:
            fh.write(ver.format(VERSION))


write_version_py()

setup(
    name="enthought_example",
    version=VERSION,
    # The entry point "force.bdss.extensions" is where the extension mechanism
    # takes place. You have to specify a path to the plugin class, as given
    # below. The name (before the '=') of the plugin is irrelevant, but try to
    # use the name of the module.
    # Also, it is good practice to use the name of your organization, like
    # we did here.
    entry_points={
        "force.bdss.extensions": [
            "enthought_example = "
            "enthought_example.example_plugin:ExamplePlugin",
            "eggbox_potential_sampler = "
            "eggbox_potential_sampler.eggbox_plugin:EggboxPlugin",
            "troughs_and_waves = "
            "troughs_and_waves.troughs_and_waves_plugin:TroughsAndWavesPlugin",
        ]
    },
    packages=find_packages(),
    install_requires=[
        "force_bdss >= 0.4.0",
    ]
)
