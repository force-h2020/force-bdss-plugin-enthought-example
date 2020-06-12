#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

from traits.api import Enum, Int
from traitsui.api import View, Item

from force_bdss.api import BaseMCOModel, PositiveInt, SCIPY_ALGORITHMS_KEYS


class MonteCarloModel(BaseMCOModel):
    """ Model class for MonteCarloMCO.
    """

    # sample or optimize
    method = Enum(['sample', 'optimize'])

    # number of samples.
    n_sample = PositiveInt(100)

    algorithms = Enum(*SCIPY_ALGORITHMS_KEYS)

    def default_traits_view(self):
        return View(
            Item("method"),
            Item("n_sample", label="No. samples"),
            Item("algorithms"),
        )
