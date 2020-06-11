#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

import logging

import random

from traits.api import Str, Instance, Enum, Int

from force_bdss.api import (
    BaseOptimizerEngine,
    IOptimizer,
    FixedMCOParameter,
    RangedMCOParameter,
    RangedVectorMCOParameter,
    ListedMCOParameter,
    CategoricalMCOParameter,
)

log = logging.getLogger(__name__)


class MonteCarloEngine(BaseOptimizerEngine):
    """



    Notes
    -----
    There is no initial value/condition/choice for categorical/level/set
    parameterization in either BDSS or Nevergrad. Therefore the optimization
    mode will not work for these.
    """

    #: Optimizer name
    name = Str("Monte Carlo")

    # sample or optimize
    method = Enum(['sample', 'optimize'])

    # number of samples.
    n_sample = Int(100)

    #: IOptimizer class that provides library backend for optimizing a
    #: callable
    optimizer = Instance(IOptimizer, transient=True)

    def optimize(self, *vargs):
        """ Generates sampling/optimization results.

        Yields
        ----------
        optimization result: tuple(np.array, np.array, list)
            Point of evaluation, objective value
        """

        if self.n_sample < 0:
            self.n_sample = -self.n_sample
        elif self.n_sample == 0:
            self.n_sample = 1

        # sample
        if self.method == 'sample':

            for _ in range(self.n_sample):

                point = self.sample()
                kpis = self._score(point)
                yield point, kpis

        # optimize
        else:

            for _ in range(self.n_sample):
                self.sample(set_initial=True)
                for point in self.optimizer.optimize_function(
                        self._score,
                        self.parameters):
                    kpis = self._score(point)
                    yield point, kpis

    def sample(self, set_initial=False):
        """ Generate random samples.

        """

        sample = []
        for param in self.parameters:

            if type(param) is FixedMCOParameter:
                sample.append(param.value)

            elif type(param) is RangedMCOParameter:
                x = random.uniform(param.lower_bound, param.upper_bound)
                sample.append(x)
                if set_initial:
                    param.initial_value = x

            elif type(param) is RangedVectorMCOParameter:
                x = [random.uniform(param.lower_bound[i],
                     param.upper_bound[i])
                     for i in range(len(param.lower_bound))]
                sample.append(x)
                if set_initial:
                    param.initial_value = x

            elif type(param) is ListedMCOParameter:
                x = random.choice(param.levels)
                sample.append(x)

            elif type(param) is CategoricalMCOParameter:
                x = random.choice(param.categories)
                sample.append(x)

        return sample
