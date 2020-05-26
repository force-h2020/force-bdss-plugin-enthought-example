#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

import math

from force_bdss.api import DataValue, Slot, BaseDataSource


class CircularWave(BaseDataSource):

    def run(self, model, parameters):
        x = parameters[0].value
        y = parameters[1].value

        rad = ((x - model.cent_x)**2.0 + (y - model.cent_y)**2.0)**0.5
        a = model.peak * math.cos(2.0 * math.pi * rad / model.wavelength)

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
