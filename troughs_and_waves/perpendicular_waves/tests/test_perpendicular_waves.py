#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.


import unittest

from unittest import mock

from traits.testing.api import UnittestTools
from force_bdss.api import DataValue, Slot, BaseDataSourceFactory

from troughs_and_waves.perpendicular_waves.perpendicular_waves import (
    PerpendicularWaves
)
from troughs_and_waves.perpendicular_waves.perpendicular_waves_model import (
    PerpendicularWavesModel
)


class TestGaussian(unittest.TestCase, UnittestTools):
    def setUp(self):
        self.factory = mock.Mock(spec=BaseDataSourceFactory)

    def test_initialization(self):
        ds = PerpendicularWaves(self.factory)
        self.assertEqual(ds.factory, self.factory)

    def test_run(self):
        ds = PerpendicularWaves(self.factory)
        model = PerpendicularWavesModel(self.factory)

        model.peak = 2.0
        model.wavelength_x = 1.0
        model.wavelength_y = 1.0

        mock_params = [
            DataValue(value=0.75),
            DataValue(value=0.75),
        ]

        result = ds.run(model, mock_params)

        self.assertAlmostEqual(result[0].value, -2.0)

    def test_slots(self):
        ds = PerpendicularWaves(self.factory)
        model = PerpendicularWaves(self.factory)
        slots = ds.slots(model)

        self.assertEqual(len(slots), 2)
        self.assertEqual(len(slots[0]), 2)
        self.assertEqual(len(slots[1]), 1)
        self.assertIsInstance(slots[0][0], Slot)
        self.assertIsInstance(slots[1][0], Slot)
