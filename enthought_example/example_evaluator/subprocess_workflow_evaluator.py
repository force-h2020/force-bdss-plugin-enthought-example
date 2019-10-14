import logging
import os
import subprocess

from traits.api import Unicode

from force_bdss.api import WorkflowEvaluator

log = logging.getLogger(__name__)


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

        return kpi_values

    def evaluate(self, parameter_values):
        """Public method to evaluate the workflow at a given set of
        MCO parameter values

        Parameters
        ----------
        parameter_values: iterable
            List of values to assign to each BaseMCOParameter defined
            in the workflow

        Returns
        -------
        kpi_results: list
            List of values corresponding to each MCO KPI in the
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
