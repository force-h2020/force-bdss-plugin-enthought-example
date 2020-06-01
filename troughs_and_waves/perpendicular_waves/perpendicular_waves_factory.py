#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

from force_bdss.api import BaseDataSourceFactory

from .perpendicular_waves_model import PerpendicularWavesModel
from .perpendicular_waves import PerpendicularWaves


class PerpendicularWavesFactory(BaseDataSourceFactory):
    def get_identifier(self):
        return "perpendicular_waves"

    def get_name(self):
        return "Perpendicular Waves"

    def get_description(self):
        return "This Data Source creates two perpendicular sine waves in " \
               "the xy-plane."

    def get_model_class(self):
        return PerpendicularWavesModel

    def get_data_source_class(self):
        return PerpendicularWaves
