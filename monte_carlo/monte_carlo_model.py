#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

from traits.api import Enum, Int
from traitsui.api import View, Item

from force_bdss.api import BaseMCOModel


class MonteCarloModel(BaseMCOModel):

    # sample or optimize
    method = Enum(['sample', 'optimize'])

    # number of samples.
    n_sample = Int(100)

    algorithms = Enum("SLSQP", "Nelder-Mead", "Powell", "CG", "BFGS",
                      "Newton-CG", "L-BFGS-B", "TNC", "COBYLA",
                      "trust-constr", "dogleg",
                      "trust-ncg", "trust-exact", "trust-krylov")

    def default_traits_view(self):
        return View(
            Item("method"),
            Item("n_sample", label="No. samples"),
            Item("algorithms"),
        )
