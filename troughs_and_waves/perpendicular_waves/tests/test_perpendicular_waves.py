#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.


import unittest

from traits.testing.api import UnittestTools
from force_bdss.api import DataValue, Slot

from troughs_and_waves.troughs_and_waves_plugin import TroughsAndWavesPlugin

from troughs_and_waves.perpendicular_waves.perpendicular_waves import (
    PerpendicularWaves
)
from troughs_and_waves.perpendicular_waves.perpendicular_waves_model import (
    PerpendicularWavesModel
)
from troughs_and_waves.perpendicular_waves.perpendicular_waves_factory import (
    PerpendicularWavesFactory
)


class TestGaussian(unittest.TestCase, UnittestTools):
    def setUp(self):
        self.plugin = TroughsAndWavesPlugin()
        self.factory = PerpendicularWavesFactory(plugin=self.plugin)
        self.ds = self.factory.create_data_source()
        self.model = self.factory.create_model()

    def test_initialization(self):
        self.assertNotEqual(self.factory.id, "")
        self.assertEqual(self.factory.plugin_id, self.plugin.id)
        self.assertIsInstance(self.ds, PerpendicularWaves)
        self.assertIsInstance(self.model, PerpendicularWavesModel)

    def test_slots(self):
        slots = self.ds.slots(self.model)
        self.assertEqual(len(slots), 2)
        self.assertEqual(len(slots[0]), 2)
        self.assertEqual(len(slots[1]), 1)
        self.assertIsInstance(slots[0][0], Slot)
        self.assertIsInstance(slots[1][0], Slot)

    def test_run(self):
        self.model.peak = 2.0
        self.model.wavelength_x = 1.0
        self.model.wavelength_y = 1.0

        mock_params = [
            DataValue(value=0.75),
            DataValue(value=0.75),
        ]

        result = self.ds.run(self.model, mock_params)
        self.assertAlmostEqual(result[0].value, -2.0)
