#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

from force_bdss.api import BaseDataSourceFactory

from .model import EggboxPESDataSourceModel
from .data_source import EggboxPESDataSource


class EggboxPESDataSourceFactory(BaseDataSourceFactory):
    """ This class provides factory methods to generate instances of
    :obj:`EggboxPESDataSource` and the associated
    :obj:`EggboxPESDataSourceModel`.

    """
    def get_identifier(self):
        return "eggbox_pes_data_source"

    def get_name(self):
        return "Random Eggbox Potential Energy Surface Data Source"

    def get_description(self):
        return ("This Data Source creates a random eggbox potential "
                "that will be optionally locally optimised at the "
                "points provided by the MCO.")

    def get_model_class(self):
        return EggboxPESDataSourceModel

    def get_data_source_class(self):
        return EggboxPESDataSource
