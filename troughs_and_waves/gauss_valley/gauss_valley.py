#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

import math

from force_bdss.api import DataValue, Slot, BaseDataSource


class GaussValley(BaseDataSource):

    def run(self, model, parameters):
        x = parameters[0].value
        y = parameters[1].value

        # rotated x coordinate (distance from valley centre)
        x_r = x * math.cos(-model.angle) - y * math.sin(-model.angle)

        a = ((x_r - model.offset) ** 2) / (2.0 * model.sigma ** 2)
        a = model.peak * math.exp(-a)

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
