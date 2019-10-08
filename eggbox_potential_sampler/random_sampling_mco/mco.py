import logging
import numpy as np

from force_bdss.api import (
    BaseMCO, DataValue
)


log = logging.getLogger(__name__)


class RandomSamplingMCO(BaseMCO):
    """ This MCO draws random samples in [0, 1] and samples a random
    eggbox potential constructed by EggboxPESDataSource. Calls to
    the BDSS can be made either as a separate subprocess, or internally.

    """
    def run(self, model, solver):
        """ Run the MCO with the desired method and communicate the
        results.

        Parameters
        ----------
        model: :obj:`RandomSamplingMCOModel`
            the model that defines MCO parameters and outputs.
        solver: WorkflowSolver
            Contains information on the Workflow and can evaluate the state
            of the KPIs for a given set of parameter values
        """
        solver.mode = model.evaluation_mode

        counter = 0
        while counter < model.num_trials:
            counter += 1
            log.info("MCO iteration {}/{}".format(counter, model.num_trials))
            trial_position = np.random.rand(len(model.parameters))

            kpis = solver.solve(trial_position)

            if len(kpis) > 0:
                weights = [1 / len(kpis)] * len(kpis)
            else:
                weights = []

            self.notify_new_point(
                [DataValue(value=v) for v in trial_position],
                kpis,
                weights
            )
