#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

from force_bdss.api import BaseDataSourceFactory

from .gauss_valley_model import GaussValleyModel
from .gauss_valley import GaussValley


class GaussValleyFactory(BaseDataSourceFactory):
    def get_identifier(self):
        return "gauss_valley"

    def get_name(self):
        return "Gaussian Valley"

    def get_description(self):
        return "This Data Source creates a valley " \
               "on the xy-plane with a Gaussian cross-section."

    def get_model_class(self):
        return GaussValleyModel

    def get_data_source_class(self):
        return GaussValley
