from force_bdss.api import BaseExtensionPlugin, plugin_id

from .eggbox_pes_data_source.factory import EggboxPESDataSourceFactory
from .random_sampling_mco.mco_factory import RandomSamplingMCOFactory
from .model_based_mco.mco_factory import ModelBasedOptimizationMCOFactory


PLUGIN_VERSION = 0


class EggboxPlugin(BaseExtensionPlugin):
    """ This plugin provides the following classes and associated
    factories:

    :obj:`EggboxPESDataSource`: a data source that defines a random PES with
    arbitrary dimensions and optionally locally optimises it at the
    points it receives.

    :obj:`RandomSamplingMCO`: an MCO that randomly samples potentials of
    arbitrary dimensions.


    """
    id = plugin_id("pes", "sampler", PLUGIN_VERSION)

    def get_name(self):
        return "Potential energy surface sampler"

    def get_description(self):
        return ("An example plugin for sampling arbitrary dimensional "
                "potential energy surfaces, developed at Enthought.")

    def get_version(self):
        return PLUGIN_VERSION

    def get_factory_classes(self):
        return [
            EggboxPESDataSourceFactory,
            RandomSamplingMCOFactory,
            ModelBasedOptimizationMCOFactory
        ]
