#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

from force_bdss.api import BaseDataSourceFactory

from .circular_wave_model import CircularWaveModel
from .circular_wave import CircularWave


class CircularWaveFactory(BaseDataSourceFactory):
    def get_identifier(self):
        return "circular_wave"

    def get_name(self):
        return "Circular Wave"

    def get_description(self):
        return "This Data Source creates a circular wave in " \
               "the xy-plane."

    def get_model_class(self):
        return CircularWaveModel

    def get_data_source_class(self):
        return CircularWave
