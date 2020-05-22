#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

import math

from force_bdss.api import DataValue, Slot, BaseDataSource


class GaussianDataSource(BaseDataSource):

    def run(self, model, parameters):
        x = parameters[0].value
        y = parameters[1].value

        a = ((x - model.cent_x)**2)/(2.0*model.sigm_x**2)
        a += ((y - model.cent_y)**2) / (2.0*model.sigm_y**2)
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
