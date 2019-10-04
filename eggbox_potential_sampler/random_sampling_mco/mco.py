import subprocess
import sys
import logging
import numpy as np

from traits.api import (
    HasStrictTraits, Instance, Interface, List, provides, Str
)

from force_bdss.api import (
    BaseMCO, DataValue, Workflow
)


log = logging.getLogger(__name__)


class RandomSamplingMCO(BaseMCO):
    """ This MCO draws random samples in [0, 1] and samples a random
    eggbox potential constructed by EggboxPESDataSource. Calls to
    the BDSS can be made either as a separate subprocess, or internally.

    """
    def run(self, model):
        """ Run the MCO with the desired method and communicate the
        results.

        Parameters
        ----------
        model: :obj:`RandomSamplingMCOModel`
            the model that defines MCO parameters and outputs.

        """
        kpis = model.kpis
        application = self.factory.plugin.application
        if model.evaluation_mode == "Subprocess":
            single_point_evaluator = SubprocessSinglePointEvaluator(
                sys.argv[0], application.workflow_file.path
            )
        else:
            single_point_evaluator = InternalSinglePointEvaluator(
                application.workflow_file.workflow,
                model.parameters
            )

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


class ISinglePointEvaluator(Interface):
    def evaluate(self, in_values):
        """ Evaluate the potential at a single point. """


@provides(ISinglePointEvaluator)
class SubprocessSinglePointEvaluator(HasStrictTraits):
    """ Spawns a subprocess to evaluate a single point. """
    evaluation_executable_path = Str()
    workflow_filepath = Str()

    def __init__(self, evaluation_executable_path, workflow_filepath):
        super(SubprocessSinglePointEvaluator, self).__init__(
            evaluation_executable_path=evaluation_executable_path,
            workflow_filepath=workflow_filepath
        )

    def evaluate(self, in_values):
        cmd = [self.evaluation_executable_path,
               "--logfile",
               "bdss.log",
               "--evaluate",
               self.workflow_filepath]

        log.info("Spawning subprocess: {}".format(cmd))
        ps = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )
        log.info("Sending values: {}".format([str(v) for v in in_values]))

        out = ps.communicate(
            " ".join([str(v) for v in in_values]).encode("utf-8"))

        log.info(
            "Received values: {}".format(
                [x for x in out[0].decode("utf-8").split()]))

        return [float(x) for x in out[0].decode("utf-8").split()]


@provides(ISinglePointEvaluator)
class InternalSinglePointEvaluator(HasStrictTraits):
    """ Evaluate the potential at a single point, without spawning a
    new process.

    """
    workflow = Instance(Workflow)
    parameters = List()

    def __init__(self, workflow, parameters):
        super(InternalSinglePointEvaluator, self).__init__(
            workflow=workflow,
            parameters=parameters
        )

    def evaluate(self, in_values):
        value_names = [p.name for p in self.parameters]
        value_types = [p.type for p in self.parameters]

        data_values = [
            DataValue(type=type_, name=name, value=value)
            for type_, name, value in zip(
                value_types, value_names, in_values)]

        kpis = self.workflow.execute(data_values)

        return [kpi.value for kpi in kpis]
