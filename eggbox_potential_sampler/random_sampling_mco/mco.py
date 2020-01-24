import logging
import sys

import numpy as np

from force_bdss.api import (
    BaseMCO, DataValue
)

from enthought_example.example_evaluator.subprocess_workflow import (
    SubprocessWorkflow
)

log = logging.getLogger(__name__)


class RandomSamplingMCO(BaseMCO):
    """ This MCO draws random samples in [0, 1] and samples a random
    eggbox potential constructed by EggboxPESDataSource. Calls to
    the BDSS can be made either as a separate subprocess, or internally.
    """
    def run(self, evaluator):
        """ Run the MCO with the desired method and communicate the
        results.
        """

        model = evaluator.mco_model

        if model.evaluation_mode == "Subprocess":
            # Here we create an instance of our WorkflowEvaluator subclass
            # that allows for evaluation of a state in the workflow via calling
            # force_bdss on a new subprocess running in 'evaluate' mode.
            # Note: a BaseMCOCommunicator must be present to pass in parameter
            # values and returning the KPI for a force_bdss run in 'evaluate'
            # mode
            single_point_evaluator = SubprocessWorkflow(
                mco_model=evaluator.mco_model,
                execution_layers=evaluator.execution_layers,
                notification_listeners=evaluator.notification_listeners,
                executable_path=sys.argv[0]
            )
        else:
            single_point_evaluator = evaluator

        counter = 0
        while counter < model.num_trials:
            counter += 1
            log.info("MCO iteration {}/{}".format(counter, model.num_trials))
            trial_position = np.random.rand(len(model.parameters))

            kpis = single_point_evaluator.evaluate(trial_position)

            self.notify_new_point(
                [DataValue(value=v) for v in trial_position],
                [DataValue(value=v) for v in kpis],
                [1 / len(kpis)] * len(kpis)
            )
