#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

from force_bdss.api import plugin_id
from force_bdss.core_plugins.base_extension_plugin import BaseExtensionPlugin

from .mco.monte_carlo_factory import MonteCarloFactory

PLUGIN_VERSION = 0


class MonteCarloPlugin(BaseExtensionPlugin):

    id = plugin_id("enthought", "monte_carlo", PLUGIN_VERSION)

    def get_name(self):
        return "Monte Carlo"

    def get_description(self):
        return "Random sampling and optimization."

    def get_version(self):
        return PLUGIN_VERSION

    #: Define the factory classes that you want to export to this list.
    def get_factory_classes(self):
        return [
            MonteCarloFactory,
        ]
