#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

import unittest

from unittest import mock

from traits.testing.api import UnittestTools
from force_bdss.api import DataValue, Slot, BaseDataSourceFactory

from troughs_and_waves.gaussian.gaussian import Gaussian
from troughs_and_waves.gaussian.gaussian_model import GaussianModel


class TestGaussianDataSource(unittest.TestCase, UnittestTools):
    def setUp(self):
        self.factory = mock.Mock(spec=BaseDataSourceFactory)

    def test_initialization(self):
        ds = Gaussian(self.factory)
        self.assertEqual(ds.factory, self.factory)

    def test_run(self):
        ds = Gaussian(self.factory)
        model = GaussianModel(self.factory)

        model.peak = -2.0
        model.cent_x = -1.0
        model.cent_y = -1.0
        model.sigm_x = 1.0
        model.sigm_y = 1.0

        mock_params = [
            DataValue(value=-1.0),
            DataValue(value=-1.0),
        ]

        result = ds.run(model, mock_params)

        self.assertAlmostEqual(result[0].value, -2.0)

    def test_slots(self):
        ds = Gaussian(self.factory)
        model = GaussianModel(self.factory)
        slots = ds.slots(model)

        self.assertEqual(len(slots), 2)
        self.assertEqual(len(slots[0]), 2)
        self.assertEqual(len(slots[1]), 1)
        self.assertIsInstance(slots[0][0], Slot)
        self.assertIsInstance(slots[1][0], Slot)
