#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

from traits.api import Float
from traitsui.api import View, Item, Group

from force_bdss.api import BaseDataSourceModel


class PerpendicularWavesModel(BaseDataSourceModel):

    peak = Float(
        2.0,
        label="Peak amplitude",
        desc="Amplitude of the peak."
    )
    wavelength_x = Float(
        1.0,
        label="x",
        desc="Wavelength along the x-axis."
    )
    wavelength_y = Float(
        1.0,
        label="y",
        desc="Wavelength along the y-axis."
    )

    traits_view = View(
        Item("peak"),
        Group(
            Item("wavelength_x"),
            Item("wavelength_y"),
            label="Wavelength"
        )
    )
