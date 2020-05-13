#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

import unittest

from eggbox_potential_sampler.eggbox_pes_data_source.data_source\
    import EggboxPESDataSource
from eggbox_potential_sampler.eggbox_pes_data_source.model\
    import EggboxPESDataSourceModel
from eggbox_potential_sampler.eggbox_plugin import EggboxPlugin


class DataSourceFactoryTestMixin(unittest.TestCase):

    def setUp(self):
        self.plugin = EggboxPlugin()
        self.factory = self.plugin.data_source_factories[0]

    def test_initialization(self):
        self.assertNotEqual(self.factory.id, "")
        self.assertEqual(self.factory.plugin_id, self.plugin.id)

    def test_create_model(self):
        model = self.factory.create_model({})
        self.assertIsInstance(model, EggboxPESDataSourceModel)

        model = self.factory.create_model()
        self.assertIsInstance(model, EggboxPESDataSourceModel)

    def test_create_data_source(self):
        ds = self.factory.create_data_source()
        self.assertIsInstance(ds, EggboxPESDataSource)
