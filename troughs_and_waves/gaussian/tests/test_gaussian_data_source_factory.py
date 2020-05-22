#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

import unittest

from troughs_and_waves.gaussian.gaussian_data_source import (
    GaussianDataSource
)

from troughs_and_waves.gaussian.gaussian_data_source_model import (
    GaussianDataSourceModel
)

from troughs_and_waves.troughs_and_waves_plugin import TroughsAndWavesPlugin


class DataSourceFactoryTestMixin(unittest.TestCase):
    def setUp(self):
        self.plugin = TroughsAndWavesPlugin()
        self.factory = self.plugin.data_source_factories[0]

    def test_initialization(self):
        self.assertNotEqual(self.factory.id, "")
        self.assertEqual(self.factory.plugin_id, self.plugin.id)

    def test_create_model(self):
        model = self.factory.create_model({})
        self.assertIsInstance(model, GaussianDataSourceModel)

        model = self.factory.create_model()
        self.assertIsInstance(model, GaussianDataSourceModel)

    def test_create_data_source(self):
        ds = self.factory.create_data_source()
        self.assertIsInstance(ds, GaussianDataSource)
