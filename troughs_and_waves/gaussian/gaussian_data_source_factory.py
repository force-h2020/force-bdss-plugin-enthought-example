#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

from force_bdss.api import BaseDataSourceFactory

from .gaussian_data_source_model import GaussianDataSourceModel
from .gaussian_data_source import GaussianDataSource


class GaussianDataSourceFactory(BaseDataSourceFactory):
    def get_identifier(self):
        return "gaussian"

    def get_name(self):
        return "Gaussian"

    def get_description(self):
        return "This Data Source creates a two-dimensional " \
               "(xy-plane) Gaussian."

    def get_model_class(self):
        return GaussianDataSourceModel

    def get_data_source_class(self):
        return GaussianDataSource
