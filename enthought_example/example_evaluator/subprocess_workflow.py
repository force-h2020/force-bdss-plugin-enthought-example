#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

import logging
import os
import subprocess
import tempfile

from traits.api import Unicode, File

from force_bdss.api import Workflow, WorkflowWriter

log = logging.getLogger(__name__)


class SubprocessWorkflow(Workflow):
    """A subclass of WorkflowSolver that spawns a subprocess to
     evaluate a single point."""

    #: File path of the Workflow object
    workflow_filepath = File(transient=True)

    #: The path to the force_bdss executable
    executable_path = Unicode(transient=True)

    def __getstate__(self):
        """Overloads the Workflow.__getstate__ method to ensure
        that no BaseNotificationListeners instances are serialised.
        Allowing so would cause duplicate messages to be sent to
        the UI from a single socket when the force_bdss is run
        on a new process."""
        data = super(SubprocessWorkflow, self).__getstate__()
        data['notification_listeners'] = []
        return data

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

    def _subprocess_evaluate(self, parameter_values, filepath):
        """Executes the workflow using the given parameter values
        running on an external process via the subprocess library.
        Values for each parameter in thw workflow to calculate a
        single point
        """

        # This command calls a force_bdss executable on another process
        # to evaluate workflow serialized in filepath at a state determined
        # by the parameter values. A BaseMCOCommunicator will be needed
        # to be defined in the workflow to receive the data and send
        # back values corresponding to each KPI via the command line.
        command = [self.executable_path,
                   "--logfile",
                   "bdss.log",
                   "--evaluate",
                   filepath]

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
            # If a path to a workflow file is assigned, then use this
            # as a reference, otherwise generate a temporary file and
            # save a copy of this Workflow instance there
            if self.workflow_filepath:
                return self._subprocess_evaluate(
                    parameter_values, self.workflow_filepath)
            else:
                with tempfile.NamedTemporaryFile() as tmp_file:
                    writer = WorkflowWriter()
                    writer.write(self, tmp_file.name)
                    return self._subprocess_evaluate(
                        parameter_values, tmp_file.name)

        except Exception:
            message = (
                'SubprocessWorkflow failed '
                'to run. This is likely due to an error in the '
                'BaseMCOCommunicator assigned to {}.'.format(
                    self.mco_model.factory.__class__)
            )
            log.exception(message)
            raise RuntimeError(message)
