#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

import unittest

from troughs_and_waves.gauss_valley.gauss_valley import GaussValley
from troughs_and_waves.gauss_valley.gauss_valley_model import GaussValleyModel

from troughs_and_waves.troughs_and_waves_plugin import TroughsAndWavesPlugin


class DataSourceFactoryTestMixin(unittest.TestCase):
    def setUp(self):
        self.plugin = TroughsAndWavesPlugin()
        self.factory = self.plugin.data_source_factories[3]

    def test_initialization(self):
        self.assertNotEqual(self.factory.id, "")
        self.assertEqual(self.factory.plugin_id, self.plugin.id)

    def test_create_model(self):
        model = self.factory.create_model({})
        self.assertIsInstance(model, GaussValleyModel)

        model = self.factory.create_model()
        self.assertIsInstance(model, GaussValleyModel)

    def test_create_data_source(self):
        ds = self.factory.create_data_source()
        self.assertIsInstance(ds, GaussValley)
