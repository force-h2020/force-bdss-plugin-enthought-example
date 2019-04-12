import unittest

from unittest import mock

from traits.testing.api import UnittestTools
from force_bdss.api import DataValue, Slot, BaseDataSourceFactory

from eggbox_potential_sampler.eggbox_pes_data_source.data_source\
    import EggboxPESDataSource

from eggbox_potential_sampler.eggbox_pes_data_source.model\
    import EggboxPESDataSourceModel


class TestEggboxPESDataSource(unittest.TestCase, UnittestTools):
    def setUp(self):
        super(TestEggboxPESDataSource, self).setUp()
        self.factory = mock.Mock(spec=BaseDataSourceFactory)

    def test_initialization(self):
        ds = EggboxPESDataSource(self.factory)
        self.assertEqual(ds.factory, self.factory)

    def test_1d_run(self):
        ds = EggboxPESDataSource(self.factory)
        model = EggboxPESDataSourceModel(self.factory)
        model.num_cells = 5
        model.dimension = 1
        model.sigma_star = 0.1

        trial = 1.0
        mock_params = [DataValue(value=trial, type="float")]
        result = ds.run(model, mock_params)
        self.assertEqual(len(model.basin_depths), 5)
        self.assertEqual(len(model.basin_positions), 5)
        self.assertEqual(len(result), 2)

        trial = 0.0
        mock_params = [DataValue(value=trial, type="float")]
        result = ds.run(model, mock_params)
        self.assertEqual(len(model.basin_depths), 5)
        self.assertEqual(len(model.basin_positions), 5)
        self.assertEqual(len(result), 2)

    def test_2d_run(self):
        ds = EggboxPESDataSource(self.factory)
        model = EggboxPESDataSourceModel(self.factory)
        model.num_cells = 3
        model.dimension = 2
        model.sigma_star = 0.5

        trial = [0, 1]
        mock_params = [DataValue(value=trial[0], type="float"),
                       DataValue(value=trial[1], type='float')]
        result = ds.run(model, mock_params)
        self.assertEqual(len(result), 3)
        self.assertEqual(len(model.basin_depths), 9)
        self.assertEqual(len(model.basin_positions), 9)

        trial = [0.2, 0.6]
        mock_params = [DataValue(value=trial[0], type="float"),
                       DataValue(value=trial[1], type='float')]
        result = ds.run(model, mock_params)
        self.assertEqual(len(result), 3)
        self.assertEqual(len(model.basin_depths), 9)
        self.assertEqual(len(model.basin_positions), 9)

    def test_out_of_bounds(self):
        ds = EggboxPESDataSource(self.factory)
        model = EggboxPESDataSourceModel(self.factory)
        model.num_cells = 3
        model.dimension = 1
        model.sigma_star = 0.5

        with self.assertRaises(RuntimeError):
            mock_params = [DataValue(value=4, type="float")]
            ds.run(model, mock_params)

    def test_slots(self):
        ds = EggboxPESDataSource(self.factory)
        model = EggboxPESDataSourceModel(self.factory)
        model.dimension = 2
        slots = ds.slots(model)
        self.assertEqual(len(slots), 2)
        self.assertEqual(len(slots[0]), 2)
        self.assertEqual(len(slots[1]), 3)
        for slot in slots[0]:
            self.assertIsInstance(slot, Slot)
        for slot in slots[1]:
            self.assertIsInstance(slot, Slot)

        model.dimension = 3
        slots = ds.slots(model)
        self.assertEqual(len(slots), 2)
        self.assertEqual(len(slots[0]), 3)
        self.assertEqual(len(slots[1]), 4)
        for slot in slots[0]:
            self.assertIsInstance(slot, Slot)
        for slot in slots[1]:
            self.assertIsInstance(slot, Slot)

        model.dimension = 1
        slots = ds.slots(model)
        self.assertEqual(len(slots), 2)
        self.assertEqual(len(slots[0]), 1)
        self.assertEqual(len(slots[1]), 2)
        for slot in slots[0]:
            self.assertIsInstance(slot, Slot)
        for slot in slots[1]:
            self.assertIsInstance(slot, Slot)

        with self.assertTraitChanges(model, 'changes_slots'):
            model.cuba_potential_type = 'volts'
            model.cuba_design_space_type = 'metre'
            model.dimension = 2
        slots = ds.slots(model)
        self.assertEqual(slots[0][0].type, 'metre')
        self.assertEqual(slots[0][1].type, 'metre')
        self.assertEqual(slots[1][0].type, 'metre')
        self.assertEqual(slots[1][1].type, 'metre')
        self.assertEqual(slots[1][2].type, 'volts')
