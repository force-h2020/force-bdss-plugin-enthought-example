#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

from unittest import TestCase, mock

from traits.testing.unittest_tools import UnittestTools

from traitsui.api import View

from force_bdss.api import (
    ScipyOptimizer,
    FixedMCOParameter,
    RangedMCOParameter,
    RangedVectorMCOParameter,
    ListedMCOParameter,
    CategoricalMCOParameter,
)

from monte_carlo.monte_carlo_plugin import MonteCarloPlugin
from monte_carlo.mco.monte_carlo_mco import MonteCarloMCO
from monte_carlo.mco.monte_carlo_factory import MonteCarloFactory
from monte_carlo.mco.monte_carlo_model import MonteCarloModel
from monte_carlo.mco.monte_carlo_engine import MonteCarloEngine
from monte_carlo.tests.workflow import ProbeWorkflow


class TestMCO(TestCase, UnittestTools):
    def setUp(self):
        self.plugin = MonteCarloPlugin()
        self.factory = self.plugin.mco_factories[0]
        self.mco = self.factory.create_optimizer()
        self.model = self.factory.create_model()

    def test_mco_model(self):
        self.assertEqual(100, self.model.n_sample)
        view = self.model.default_traits_view()
        self.assertIsInstance(view, View)

    def test_mco_factory(self):
        self.assertIsInstance(self.factory, MonteCarloFactory)
        self.assertEqual("monte_carlo_mco", self.factory.get_identifier())
        self.assertIs(self.factory.get_model_class(), MonteCarloModel)
        self.assertIs(self.factory.get_optimizer_class(), MonteCarloMCO)
        self.assertEqual(5, len(self.factory.get_parameter_factory_classes()))

    def test_sampling(self):

        param = [
            FixedMCOParameter(value=0.0, factory=None),
            RangedMCOParameter(
                initial_value=0.0,
                lower_bound=-1.0,
                upper_bound=1.0,
                factory=None
            ),
            RangedVectorMCOParameter(
                initial_value=[0.0, 0.0],
                lower_bound=[-1.0, -1.0],
                upper_bound=[1.0, 1.0],
                factory=None
            ),
            ListedMCOParameter(levels=[0.0, 1.0], factory=None),
            CategoricalMCOParameter(categories=['a', 'b'], factory=None),
        ]

        engine = MonteCarloEngine(
            single_point_evaluator=ProbeWorkflow(),
            parameters=param,
            kpis=self.model.kpis,
            method='sample',
            n_sample=100,
            optimizer=None
        )

        # test sampling
        for (point, kpis) in engine.optimize():
            # fixed is fixed
            self.assertEqual(point[0], 0.0)
            # ranged is in range
            self.assertGreaterEqual(point[1], -1.0)
            self.assertLessEqual(point[1], 1.0)
            # ranged vector is in range
            self.assertGreaterEqual(point[2][0], -1.0)
            self.assertLessEqual(point[2][0], 1.0)
            # listed
            self.assertIn(point[3], [0.0, 1.0])
            # categorical
            self.assertIn(point[4], ['a', 'b'])

    def test_optimization(self):
        """ Only checking that initial values are set correctly. Not
        actually checking the optimization result.
        """

        # Scipy optimizer can only take these parametrizations.
        param = [
            RangedMCOParameter(
                initial_value=0.0,
                lower_bound=-1.0,
                upper_bound=1.0,
                factory=None
            ),
            RangedVectorMCOParameter(
                initial_value=[0.0, 0.0],
                lower_bound=[-1.0, -1.0],
                upper_bound=[1.0, 1.0],
                factory=None
            ),
        ]

        optimizer = ScipyOptimizer()

        engine = MonteCarloEngine(
            single_point_evaluator=ProbeWorkflow(),
            parameters=param,
            kpis=self.model.kpis,
            method='optimize',
            n_sample=1,
            optimizer=optimizer
        )

        # test initial value setting
        for (point, kpis) in engine.optimize():
            # ranged is in range
            self.assertGreaterEqual(engine.parameters[0].initial_value, -1.0)
            self.assertLessEqual(engine.parameters[0].initial_value, 1.0)
            # ranged vector is in range
            self.assertGreaterEqual(
                engine.parameters[1].initial_value[0], -1.0
            )
            self.assertLessEqual(
                engine.parameters[1].initial_value[0], 1.0
            )
