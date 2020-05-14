#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

import sys

from force_bdss.api import (
    BaseMCOCommunicator,
    DataValue)


class ExampleMCOCommunicator(BaseMCOCommunicator):
    """The communicator is responsible for handing the communication protocol
    between the MCO executable (for example, the dakota executable) and the
    single point evaluation (our BDSS in --evaluate mode).

    This MCO communicator assumes that the communication happens via stdin
    and stdout, which is what dakota does when invoking an external program
    to perform a single point evaluation.
    """
    def receive_from_mco(self, model):
        """Receives data from the MCO (e.g. dakota) by reading from
        standard input the sequence of numbers that are this execution's
        parameter values.

        You can use fancier communication systems here if your MCO supports
        them.
        """
        data = sys.stdin.read()
        values = list(map(float, data.split()))
        value_names = [p.name for p in model.parameters]
        value_types = [p.type for p in model.parameters]

        # The values must be given a type. The MCO may pass raw numbers
        # with no type information. You are free to use metadata your MCO may
        # provide, but it is not mandatory that this data is available. You
        # can also use the model specification itself.
        # In any case, you must return a list of DataValue objects.
        return [
            DataValue(type=type_, name=name, value=value)
            for type_, name, value in zip(
                value_types, value_names, values)]

    def send_to_mco(self, model, data_values):
        """This method does the reverse. Once the single point evaluation
        is completed, this method is used to send the data back to the MCO.
        We assume in this case it's done via stdout, but you can use whatever
        your MCO may support.

        You will receive a list of data values that are your KPIs as exiting
        from the evaluation pipeline.
        """
        data = " ".join([str(dv.value) for dv in data_values])
        sys.stdout.write(data)
