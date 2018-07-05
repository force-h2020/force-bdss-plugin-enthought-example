import subprocess
import sys
import itertools
import collections

from force_bdss.api import BaseMCO


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
    - report new events as they happen, specifically::
      - when the MCO starts its execution, set::

           self.started = True

      - when the MCO has computed a new result. Set new_data with a
        dictionary, as indicated::

            self.new_data = {
                'input': tuple(input_parameter_values),
                'output': tuple(output_kpi_values)
            }

      - when the MCO ends its execution, set::

            self.finished = True

    Currently there's no error handling.
    """
    def run(self, model):
        # This implementation mimics the expected behavior of dakota
        # by spawning the force_bdss with the evaluate option to compute
        # a single point. Your specific implementation should be quite
        # different, in the sense that it is supposed to spawn your MCO
        # as a separate process, collect its results via stdout or any
        # other more appropriate channel, and notify using the mechanisms
        # explained above.
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

        application = self.factory.plugin.application

        # Inform that the evaluation has started. Missing this is a crime.
        self.started = True

        for value in value_iterator:
            # Spawn the single point evaluation, which is the bdss itself
            # with the option evaluate.
            # We pass the specific parameter values via stdin, and read
            # the result via stdout. The format is decided by the
            # MCOCommunicator. NOTE: The communicator is involved in the
            # communication between the MCO executable and the bdss single
            # point evaluation, _not_ between the bdss and the MCO executable.
            ps = subprocess.Popen(
                [sys.argv[0],
                 "--evaluate",
                 application.workflow_filepath],
                stdout=subprocess.PIPE,
                stdin=subprocess.PIPE)

            out = ps.communicate(
                " ".join([str(v) for v in value]).encode("utf-8"))
            out_data = out[0].decode("utf-8").split()

            # When there is new data, this operation informs the system that
            # new data has been received. It must be a dictionary as given.
            self.new_data = {
                'input': tuple(value),
                'output': tuple(out_data)
            }

        # To inform the rest of the system that the evaluation has completed.
        # we set this event to True
        self.finished = True