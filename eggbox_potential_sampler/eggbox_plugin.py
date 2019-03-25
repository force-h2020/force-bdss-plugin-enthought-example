from force_bdss.api import BaseExtensionPlugin, plugin_id

from .eggbox_pes_data_source.factory import EggboxPESDataSourceFactory
from .random_sampling_mco.mco_factory import RandomSamplingMCOFactory

PLUGIN_VERSION = 0


class EggboxPlugin(BaseExtensionPlugin):
    """ This plugin provides the following classes and associated
    factories:

    - PESDataSource: a data source that defines a random PES with
    arbitrary dimensions and locally optimises it at the points
    it receives.
    - RandomSamplingMCO: an MCO that randomly samples potentials of
    arbitrary dimensions.

    """
    #: Define the id of the plugin by calling the plugin_id function, and
    #: passing three information:
    #: - the producer: a unique string identifying the company or research
    #: institute.
    #: - the plugin identifier: a unique string identifying the plugin.
    #: - the version number of the plugin, as an integer.
    id = plugin_id("pes", "sampler", PLUGIN_VERSION)

    def get_name(self):
        return "Potential energy surface sampler"

    def get_description(self):
        return ("An example plugin for sampling arbitrary dimensional "
                "potential energy surfaces, developed by Enthought.")

    def get_version(self):
        return PLUGIN_VERSION

    #: Define the factory classes that you want to export to this list.
    def get_factory_classes(self):
        return [
            EggboxPESDataSourceFactory,
            RandomSamplingMCOFactory
        ]
