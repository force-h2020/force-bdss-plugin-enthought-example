#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

from traits.api import Float
from traitsui.api import View, Item

from force_bdss.api import BaseDataSourceModel


class GaussValleyModel(BaseDataSourceModel):

    peak = Float(
        2.0,
        label="Peak amplitude",
        desc="Amplitude of the peak."
    )
    angle = Float(
        3.14,
        label="Angle",
        desc="Angle of valley (in radians)."
    )
    offset = Float(
        0.0,
        label="Offset",
        desc="Offset of valley from origin."
    )
    sigma = Float(
        1.0,
        label="Sigma",
        desc="Width (standard deviation) of valley."
    )

    traits_view = View(
        Item("peak"),
        Item("angle"),
        Item("offset"),
        Item("sigma"),
    )
