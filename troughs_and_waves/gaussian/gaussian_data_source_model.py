#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

from traits.api import Float
from traitsui.api import View, Item

from force_bdss.api import BaseDataSourceModel


class GaussianDataSourceModel(BaseDataSourceModel):

    peak = Float(
        -2.0,
        label="Peak amplitude",
        desc="Amplitude of the peak."
    )
    cent_x = Float(
        -1.0,
        label="Center (x)",
        desc="x coordinate of the peak."
    )
    cent_y = Float(
        -1.0,
        label="Centre (y)",
        desc="y coordinate of the peak."
    )
    sigm_x = Float(
        0.6,
        label="Sigma (x)",
        desc="Width (standard deviation) along the x-axis."
    )
    sigm_y = Float(
        0.6,
        label="Sigma (y)",
        desc="Width (standard deviation) along the y-axis."
    )

    traits_view = View(
        Item("peak"),
        Item("cent_x"),
        Item("cent_y"),
        Item("sigm_x"),
        Item("sigm_y"),
    )
