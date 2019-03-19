import subprocess
import sys
import itertools
import collections
import os

from force_bdss.api import BaseMCO, DataValue


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

        for value in value_iterator:
            # Setting ETS_TOOLKIT=null before executing bdss prevents it
            # from trying to create GUI every call, giving reducing the
            # overhead by a factor of 2.
            env = {**os.environ, "ETS_TOOLKIT": "null"}
            # Spawn the single point evaluation, which is the bdss itself
            # with the option evaluate.
            # We pass the specific parameter values via stdin, and read
            # the result via stdout. The format is decided by the
            # MCOCommunicator. NOTE: The communicator is involved in the
            # communication between the MCO executable and the bdss single
            # point evaluation, _not_ between the bdss and the MCO executable.
            cmd = [sys.argv[0], "--evaluate", application.workflow_filepath]
            ps = subprocess.Popen(
                cmd, env=env, stdout=subprocess.PIPE, stdin=subprocess.PIPE)

            out = ps.communicate(
                " ".join([str(v) for v in value]).encode("utf-8"))
            out_data = out[0].decode("utf-8").split()

            # When there is new data, this operation informs the system that
            # new data has been received. It must be a dictionary as given.
            self.notify_new_point([DataValue(value=v) for v in value],
                                  [DataValue(value=v) for v in out_data],
                                  [1.0/len(out_data)]*len(out_data))
