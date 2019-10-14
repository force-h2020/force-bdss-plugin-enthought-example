import numpy as np

from traits.api import Bool, Float, List, on_trait_change, Unicode
from traitsui.api import Item, View

from force_bdss.api import BaseDataSourceModel, PositiveInt


class EggboxPESDataSourceModel(BaseDataSourceModel):
    """ This model stores all the data required to compute the
    potential. All randomness must be contained in the model, not at
    the instance-level. Changing any of the parameters used to generate
    the potential will generate an entirely new random potential.

    """

    # traits controlled by user
    dimension = PositiveInt(
        2,
        label='Dimensionality',
        changes_slots=True
    )
    cuba_design_space_type = Unicode(
        changes_slots=True,
        label='Parameter space type/units'
    )
    cuba_potential_type = Unicode(
        changes_slots=True,
        label='Potential type'
    )
    num_cells = PositiveInt(
        5,
        label='Number of cells',
        desc='Number of lattice points in each direction'
    )
    sigma_star = Float(
        0.1,
        label='σ*',
        desc='Variance of basin depths: σ*~0 will lead to identical basins '
             'σ*~1 normally lead to a few basins dominating'
    )
    locally_optimize = Bool(
        True,
        label='Locally optimize trials?',
        desc='Whether or not to locally optimize each '
             'trial and return the local minima'
    )

    # traits set by calculation
    basin_depths = List()
    basin_positions = List()

    # these lists can be useful for debugging and plotting, they contain
    # the trial values and results at each step of the MCO (see
    # `scripts/`)
    trials = List()
    results = List()

    traits_view = View([Item('locally_optimize'),
                        Item('sigma_star'),
                        Item('num_cells'),
                        Item('dimension'),
                        Item('cuba_design_space_type'),
                        Item('cuba_potential_type')])

    def __init__(self, *args, **kwargs):
        super(EggboxPESDataSourceModel, self).__init__(*args, **kwargs)
        self._set_basin_positions()
        self._randomise_model_data()

    @on_trait_change('sigma_star,basin_positions')
    def _randomise_model_data(self):
        """ Assign random depths to defined basins, with variance
        controlled by self.sigma_star.

        """
        self.basin_depths = ((self.sigma_star *
                              np.random.rand(len(self.basin_positions)))
                             .tolist())

    @on_trait_change('num_cells,dimension')
    def _set_basin_positions(self):
        """ Construct the array of basin positions for the given lattice.
        The square lattice is the only one implemented in this example.

        """
        self._set_basin_positions_square_lattice()

    def _set_basin_positions_square_lattice(self):
        """ Set the basin positions to a square lattice from 0 -> 1. """
        grids = self.dimension * [np.linspace(0, 1,
                                              num=self.num_cells,
                                              endpoint=False)]

        self.basin_positions = ((np.asarray(np.meshgrid(*grids))
                                 .reshape(self.dimension, -1).T)
                                .tolist())
