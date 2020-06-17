#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

import logging
import sys

from force_bdss.api import (
    BaseMCO,
    DataValue,
    ScipyOptimizer
)

from .monte_carlo_engine import MonteCarloEngine


log = logging.getLogger(__name__)


class MonteCarloMCO(BaseMCO):
    """ MCO using the Monte-Carlo Engine with the Scipy optimizer.

    Notes
    -----
    See the description of the engine (MonteCarloEngine).
    """

    def run(self, evaluator):

        model = evaluator.mco_model

        optimizer = ScipyOptimizer(algorithms=model.algorithms)

        engine = MonteCarloEngine(
            single_point_evaluator=evaluator,
            parameters=model.parameters,
            kpis=model.kpis,
            method=model.method,
            n_sample=model.n_sample,
            optimizer=optimizer
        )

        formatter = logging.Formatter(
            fmt='%(asctime)s %(levelname)-8s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S')
        screen_handler = logging.StreamHandler(stream=sys.stdout)
        screen_handler.setFormatter(formatter)
        log.addHandler(screen_handler)

        for index, (optimal_point, optimal_kpis) \
                in enumerate(engine.optimize()):
            # When there is new data, this operation informs the system that
            # new data has been received. It must be a dictionary as given.
            log.info("Doing  MCO run # {}".format(index))
            model.notify_progress_event(
                [DataValue(value=v) for v in optimal_point],
                [DataValue(value=v) for v in optimal_kpis],
            )
