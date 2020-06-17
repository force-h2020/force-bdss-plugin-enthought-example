#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

from traits.api import Instance, provides

from force_bdss.api import IEvaluator


from monte_carlo.mco.monte_carlo_model import MonteCarloModel


@provides(IEvaluator)
class ProbeWorkflow:

    mco_model = Instance(MonteCarloModel)

    def evaluate(self, parameter_values):
        return [0.0, 0.0]
