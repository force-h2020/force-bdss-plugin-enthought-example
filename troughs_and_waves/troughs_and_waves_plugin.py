#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

from force_bdss.api import plugin_id
from force_bdss.core_plugins.base_extension_plugin import BaseExtensionPlugin

from .gaussian.gaussian_factory import GaussianFactory
from .perpendicular_waves.perpendicular_waves_factory import (
    PerpendicularWavesFactory
)
from .circular_wave.circular_wave_factory import CircularWaveFactory
from .gauss_valley.gauss_valley_factory import GaussValleyFactory

PLUGIN_VERSION = 0


class TroughsAndWavesPlugin(BaseExtensionPlugin):
    """ Contributes data-sources useful for testing optimizers.
    It is useful to test optimizers with "ground-truth" objective functions
    where the minima, maxima and Pareto set are known.
    This plugin contributes several such functions as data-sources which
    can be used alone or mix-and-matched to create multi-objective functions.
    The data-sources involve Gaussians, sine-waves, steps and slopes.
    """
    id = plugin_id("enthought", "troughs_waves", PLUGIN_VERSION)

    def get_name(self):
        return "Troughs and Waves"

    def get_description(self):
        return "Useful data sources for testing optimizers."

    def get_version(self):
        return PLUGIN_VERSION

    #: Define the factory classes that you want to export to this list.
    def get_factory_classes(self):
        return [
            GaussianFactory,
            PerpendicularWavesFactory,
            CircularWaveFactory,
            GaussValleyFactory,
        ]
