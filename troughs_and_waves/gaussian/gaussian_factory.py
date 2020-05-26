#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

from force_bdss.api import BaseDataSourceFactory

from .gaussian_model import GaussianModel
from .gaussian import Gaussian


class GaussianFactory(BaseDataSourceFactory):
    def get_identifier(self):
        return "gaussian"

    def get_name(self):
        return "Gaussian"

    def get_description(self):
        return "This Data Source creates a two-dimensional " \
               "(xy-plane) Gaussian."

    def get_model_class(self):
        return GaussianModel

    def get_data_source_class(self):
        return Gaussian
