#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

import logging

import random

from traits.api import Str, Instance, Enum, Int

from force_bdss.api import (
    BaseOptimizerEngine,
    IOptimizer,
    PositiveInt,
    FixedMCOParameter,
    RangedMCOParameter,
    RangedVectorMCOParameter,
    ListedMCOParameter,
    CategoricalMCOParameter,
)

log = logging.getLogger(__name__)


class MonteCarloEngine(BaseOptimizerEngine):
    """ Ane engine for random (Monte Carlo) sampling and optimization.

    Extended Summary
    ----------------
    To get a picture of the overall parameter-space the user might want to
    randomly sample points. If the parameter-space contains many local
    minima (or maxima) the user might want to optimize from multiple random
    initial points, to discover those locals.

    Notes
    -----
    To find local minima/maxima it only makes sense to use a single-criterion
    optimizer (such as Scipy) or a priori multi-criterion optimizer:
    a posteriori multi-criterion optimizers usually set initial points
    themselves.
    There is no initial value/condition/choice for categorical/level/set
    parameterization in either BDSS or Nevergrad. Therefore the optimization
    mode will not work for these.
    """

    #: Optimizer name
    name = Str("Monte Carlo")

    # sample or optimize
    method = Enum(['sample', 'optimize'])

    # number of samples/initial-points.
    n_sample = PositiveInt(100)

    #: IOptimizer class, provides library backend for optimizing a callable
    optimizer = Instance(IOptimizer, transient=True)

    def optimize(self, *vargs):
        """ Generates sampling/optimization results.

        Yields
        ----------
        optimization result: tuple(np.array, np.array, list)
            Point of evaluation, objective value
        """

        # Sample
        if self.method == 'sample':

            # loop through sample points
            for _ in range(self.n_sample):

                # get point
                point = self.sample()

                # yield point and KPIs
                kpis = self._score(point)
                yield point, kpis

        # Optimize
        else:

            # loop through initial points
            for _ in range(self.n_sample):

                # set initial point
                self.sample(set_initial=True)

                # yield optimial point and KPIs (should yield once)
                for point in self.optimizer.optimize_function(
                        self._score,
                        self.parameters):
                    kpis = self._score(point)
                    yield point, kpis

    def sample(self, set_initial=False):
        """ Generate a random point in parameter space.

        Parameters
        ----------
        set_initial: bool
            Also set the initial points/conditions of the parametrization.

        Returns
        -------
        list of Any
            The random point in parameter-space.

        Notes
        -----
        There is no initial value/condition/choice for categorical/level/set
        parameterization in either BDSS or Nevergrad. Therefore
        set_initial=True will do nothing fot these.
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
