#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.


import unittest

from traits.testing.api import UnittestTools
from force_bdss.api import DataValue, Slot

from troughs_and_waves.gauss_valley.gauss_valley import GaussValley
from troughs_and_waves.gauss_valley.gauss_valley_model import (
    GaussValleyModel
)
from troughs_and_waves.gauss_valley.gauss_valley_factory import (
    GaussValleyFactory
)


class TestGaussian(unittest.TestCase, UnittestTools):
    def setUp(self):
        self.factory = GaussValleyFactory(
            plugin={'id': '0', 'name': 'test'})
        self.ds = self.factory.create_data_source()
        self.model = self.factory.create_model()

    def test_initialization(self):
        self.assertNotEqual(self.factory.id, "")
        self.assertIsInstance(self.ds, GaussValley)
        self.assertIsInstance(self.model, GaussValleyModel)

    def test_slots(self):
        slots = self.ds.slots(self.model)
        self.assertEqual(len(slots), 2)
        self.assertEqual(len(slots[0]), 2)
        self.assertEqual(len(slots[1]), 1)
        self.assertIsInstance(slots[0][0], Slot)
        self.assertIsInstance(slots[1][0], Slot)

    def test_run(self):
        self.model.peak = -2.0
        self.model.angle = 3.1415926/2.0
        self.model.offset = 0.0
        self.model.sigma = 1.0

        mock_params = [
            DataValue(value=1.0),
            DataValue(value=0.0),
        ]

        result = self.ds.run(self.model, mock_params)
        self.assertAlmostEqual(result[0].value, -2.0)
