#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

import math

from force_bdss.api import DataValue, Slot, BaseDataSource


class PerpendicularWaves(BaseDataSource):

    def run(self, model, parameters):
        x = parameters[0].value
        y = parameters[1].value

        a = math.sin(2 * math.pi * x / model.wavelength_x)
        a += math.sin(2 * math.pi * y / model.wavelength_y)
        a *= model.peak/2.0

        return [
            DataValue(value=a, type="AMPLITUDE"),
        ]

    def slots(self, model):
        return (
            (
                Slot(description="x", type="COORDINATE"),
                Slot(description="y", type="COORDINATE"),
            ),
            (
                Slot(description="a", type="AMPLITUDE"),
            )
        )
