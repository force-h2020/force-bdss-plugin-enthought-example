#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.


import unittest

from unittest import mock

from traits.testing.api import UnittestTools
from force_bdss.api import DataValue, Slot, BaseDataSourceFactory

from troughs_and_waves.circular_wave.circular_wave import CircularWave
from troughs_and_waves.circular_wave.circular_wave_model import (
    CircularWaveModel
)


class TestGaussian(unittest.TestCase, UnittestTools):
    def setUp(self):
        self.factory = mock.Mock(spec=BaseDataSourceFactory)

    def test_initialization(self):
        ds = CircularWave(self.factory)
        self.assertEqual(ds.factory, self.factory)

    def test_run(self):
        ds = CircularWave(self.factory)
        model = CircularWaveModel(self.factory)

        model.peak = 2.0
        model.cent_x = 0.0
        model.cent_y = 0.0
        model.wavelength = 1.0

        mock_params = [
            DataValue(value=0.5),
            DataValue(value=0.0),
        ]

        result = ds.run(model, mock_params)

        self.assertAlmostEqual(result[0].value, -2.0)

    def test_slots(self):
        ds = CircularWave(self.factory)
        model = CircularWaveModel(self.factory)
        slots = ds.slots(model)

        self.assertEqual(len(slots), 2)
        self.assertEqual(len(slots[0]), 2)
        self.assertEqual(len(slots[1]), 1)
        self.assertIsInstance(slots[0][0], Slot)
        self.assertIsInstance(slots[1][0], Slot)
