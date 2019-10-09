import collections
import itertools
import logging
import os
import subprocess
import sys

from traits.api import Unicode

from force_bdss.api import BaseMCO, DataValue
from force_bdss.app.workflow_evaluator import WorkflowEvaluator

log = logging.getLogger(__name__)


def rotated_range(start, stop, starting_value):
    """Produces a range of integers, then rotates so that the starting value
    is starting_value"""
    r = list(range(start, stop))
    start_idx = r.index(starting_value)
    d = collections.deque(r)
    d.rotate(-start_idx)
    return list(d)


class ExampleMCO(BaseMCO):
    """
    This class is where the MCO execution takes place. According to our
    execution model, this class is responsible for

    - generate an appropriate input file for the MCO program.
      To do so, it will use the model data, which includes both the
      instances of the parameters the user wants, and any additional
      configuration as specified in the MCO model.
    - spawn the external MCO program as a separate process and wait until
      it is completed
    - monitor its output (e.g. via standard output) as new points are
      generated
    - report new events as they happen, specifically, when the MCO has
      computed a new result, it can be broadcast with the notify_new_point::

            self.notify_new_point(
                optimal_point=[
                    DataValue(value=parameter_1),
                    DataValue(value=parameter_2),
                    DataValue(value=parameter_3)
                ],
                optimal_kpis=[
                    DataValue(value=kpi_1),
                    DataValue(value=kpi_2),
                ],
                weights=[
                    kpi_weight_1,
                    kpi_weight_2
                ]
            }

    Currently there's no error handling.
    """
    def run(self, evaluator):
        # This implementation mimics the expected behavior of dakota
        # by spawning the force_bdss with the evaluate option to compute
        # a single point. Your specific implementation should be quite
        # different, in the sense that it is supposed to spawn your MCO
        # as a separate process, collect its results via stdout or any
        # other more appropriate channel, and notify using the mechanisms
        # explained above.
        model = evaluator.mco_model

        parameters = model.parameters

        # Generate specific parameter values as from the specification in
        # the model. It basically combines all the ranges and generate points
        # in those ranges.
        values = []
        for p in parameters:
            values.append(
                rotated_range(int(p.lower_bound),
                              int(p.upper_bound),
                              int(p.initial_value))
            )

        value_iterator = itertools.product(*values)

        # Here we create an instance of our WorkflowEvaluator subclass
        # that allows for evaluation of a state in the workflow via calling
        # force_bdss on a new subprocess running in 'evaluate' mode.
        # Note: a BaseMCOCommunicator must be present to pass in parameter
        # values and returning the KPI for a force_bdss run in 'evaluate'
        # mode
        single_point_evaluator = SubprocessWorkflowEvaluator(
            workflow=evaluator.workflow,
            workflow_filepath=evaluator.workflow_filepath,
            executable_path=sys.argv[0]
        )

        for value in value_iterator:
            # We pass the specific parameter values via stdin, and read
            # the result via stdout. The format is decided by the
            # MCOCommunicator. NOTE: The communicator is involved in the
            # communication between the MCO executable and the bdss single
            # point evaluation, _not_ between the bdss and the MCO executable.
            kpis = single_point_evaluator.evaluate(value)

            if len(kpis) > 0:
                weights = [1 / len(kpis)] * len(kpis)
            else:
                weights = []

            # When there is new data, this operation informs the system that
            # new data has been received. It must be a dictionary as given.
            self.notify_new_point([DataValue(value=v) for v in value],
                                  kpis,
                                  weights)


class SubprocessWorkflowEvaluator(WorkflowEvaluator):
    """A subclass of WorkflowSolver that spawns a subprocess to
     evaluate a single point."""

    #: The path to the force_bdss executable
    executable_path = Unicode()

    def _call_subprocess(self, command, user_input):
        """Calls a subprocess to perform a command with parsed
        user_input"""

        log.info("Spawning subprocess: {}".format(command))

        # Setting ETS_TOOLKIT=null before executing bdss prevents it
        # from trying to create GUI every call, giving reducing the
        # overhead by a factor of 2.
        env = {**os.environ, "ETS_TOOLKIT": "null"}

        # Spawn the single point evaluation, which is the bdss itself
        # with the option evaluate.
        # We pass the specific parameter values via stdin, and read
        # the result via stdout.
        process = subprocess.Popen(
            command,
            env=env,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        log.info("Sending values: {}".format(user_input))
        stdout, stderr = process.communicate(
            " ".join(user_input).encode("utf-8")
        )

        return stdout

    def _subprocess_evaluate(self, parameter_values):
        """Executes the workflow using the given parameter values
        running on an external process via the subprocess library.
        Values for each parameter in thw workflow to calculate a
        single point
        """

        # This command calls a force_bdss executable on another process
        # to evaluate the same workflow at a state determined by the
        # parameter values. A BaseMCOCommunicator will be needed to be
        # defined in the workflow to receive the data and send back values
        # corresponding to each KPI via the command line.
        command = [self.executable_path,
                   "--logfile",
                   "bdss.log",
                   "--evaluate",
                   self.workflow_filepath]

        # Converts the parameter values to a string to send via
        # subprocess
        string_values = [str(v) for v in parameter_values]

        # Call subprocess to perform executable with user input
        stdout = self._call_subprocess(command, string_values)

        # Decode stdout into KPI float values
        kpi_values = [float(x) for x in stdout.decode("utf-8").split()]

        # Convert values into DataValues
        kpi_results = [
            DataValue(name=kpi.name,
                      value=value)
            for kpi, value in zip(
                self.mco_model.kpis, kpi_values)]

        return kpi_results

    def evaluate(self, parameter_values):
        """Public method to evaluate the workflow at a given set of
        MCO parameter values

        Parameters
        ----------
        parameter_values: List(Float)
            List of values to assign to each BaseMCOParameter defined
            in the workflow

        Returns
        -------
        kpi_results: List(DataValue)
            List of DataValues corresponding to each MCO KPI in the
            workflow
        """

        try:
            return self._subprocess_evaluate(parameter_values)

        except Exception:
            message = (
                'SubprocessWorkflowEvaluator failed '
                'to run. This is likely due to an error in the '
                'BaseMCOCommunicator assigned to {}.'.format(
                    self.mco_model.factory.__class__)
            )
            log.exception(message)
            raise RuntimeError(message)
