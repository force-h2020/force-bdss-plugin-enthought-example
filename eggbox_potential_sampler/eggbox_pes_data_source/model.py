import numpy as np
from traits.api import Unicode, Enum, Float, List, on_trait_change, Bool
from traitsui.api import Item, View
from force_bdss.api import BaseDataSourceModel, PositiveInt


class EggboxPESDataSourceModel(BaseDataSourceModel):
    """ This model needs to store all the data required to
    compute the potential. All randomness must be contained
    in the model, not at the instance-level.

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
        2,
        label='Number of cells',
        desc='Number of lattice points in each direction'
    )
    sigma_star = Float(
        label='σ*',
        desc='Variance of basin depths: σ*~0 will lead to identical basins '
             'σ*~1 will normally lead to one basin dominating'
    )
    locally_optimize = Bool(
        True,
        label='Locally optimize trials?',
        desc='Whether or not to locally optimize each '
             'trial and return the local minima'
    )
    lattice = Enum('Square lattice', label='Lattice type')

    # traits set by calculation
    basin_depths = List
    basin_positions = List
    trials = List
    results = List

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

    @on_trait_change('lattice, num_cells, dimension')
    def _set_basin_positions(self):
        """ Construct the array of basin positions for the given lattice. """
        if self.lattice == 'Square lattice':
            self._set_basin_positions_square_lattice()
        else:
            raise NotImplementedError('Lattice {} not implemented.'
                                      .format(self.lattice))

    def _set_basin_positions_square_lattice(self):
        """ Set the basin positions to a square lattice from 0 -> 1. """
        grids = self.dimension * [np.linspace(0, 1,
                                              num=self.num_cells,
                                              endpoint=False)]

        self.basin_positions = ((np.asarray(np.meshgrid(*grids))
                                 .reshape(self.dimension, -1).T)
                                .tolist())
