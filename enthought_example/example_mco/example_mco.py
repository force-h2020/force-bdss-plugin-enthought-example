import collections
import itertools
import logging
import sys

from force_bdss.api import BaseMCO, DataValue

from enthought_example.example_evaluator.subprocess_workflow import (
    SubprocessWorkflow
)

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

            evaluator.mco_model.notify_new_point(
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
        single_point_evaluator = SubprocessWorkflow(
            mco_model=evaluator.mco_model,
            execution_layers=evaluator.execution_layers,
            notification_listeners=evaluator.notification_listeners,
            executable_path=sys.argv[0]
        )

        for value in value_iterator:
            # We pass the specific parameter values via stdin, and read
            # the result via stdout. The format is decided by the
            # MCOCommunicator. NOTE: The communicator is involved in the
            # communication between the MCO executable and the bdss single
            # point evaluation, _not_ between the bdss and the MCO executable.
            kpis = single_point_evaluator.evaluate(value)

            # When there is new data, this operation informs the system that
            # new data has been received. It must be a dictionary as given.
            single_point_evaluator.mco_model.notify_progress_event(
                [DataValue(value=v) for v in value],
                [DataValue(value=v) for v in kpis]
            )
