#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

import itertools

import numpy as np
import scipy.optimize

from force_bdss.api import BaseDataSource, DataValue, Slot


class EggboxPESDataSource(BaseDataSource):
    """ Samples a random 2D potential energy surface (PES) with
    Gaussian distributed eggbox basins, following the work of Massen et
    al. [1].

    The parameters of the potential are defined by the DataSourceModel.
    Each trial point will be locally optimised with SciPy to its local
    minimum, unless the `locally_optimize` has been set to false in
    the model.

    Basin depths are drawn from a zero-mean Gaussian parameterised by
    dimensionless width sigma*. These basins are placed on the specified
    lattice. The height of the PES at a given point is the lowest energy
    across all basins at that point, with periodic boundary conditions.

    Note
    ----
    Following the notation of [1], this implmentation assumes a = k = 1
    and works in length units of a and energy units of k a^2.

    [1]. Exploring the origins of the power-law properties of energy
    landscapes: An egg-box model.
    arXiv:cond-mat/0612205 & 10.1016/j.physa.2007.04.054.

    Attributes
    ----------
    surface: Array
        traits Array containing the pre-mapped PES for plotting.
    lattice: Array
        traits Array containing the lattice points.
    energies: Array
        traits Array containing basin depths.

    """

    @staticmethod
    def evaluate_potential(trial, model):
        """ Evaluate the value of the potential at trial point.

        Parameters
        ----------
        trial: Array
            the position at which to evaluate the potential.
        model: :obj:`EggboxPESDataSourceModel`
            the model containing the parameters of the PES.

        Returns
        -------
        float:
            the value of the potential at the trial point.

        """
        basin_positions = np.asarray(model.basin_positions)
        basin_depths = np.asarray(model.basin_depths)

        return EggboxPESDataSource.calculate_pbc_potential(
            trial, basin_positions, basin_depths)

    @staticmethod
    def calculate_pbc_potential(trial, basin_positions, basin_depths):
        """ Calculate an N-dimensional egg-box potential in PBCs
        at a given position from the set of M basin depths and positions.

        Parameters
        ----------
        trial: numpy.ndarray
            (N, ) array containing the trial position.
        basin_positions: numpy.ndarray
            (M, N) array containing the positions of each of the M basins.
        basin_depths: numpy.ndarray
            (M, ) array containing the depth of each basin.

        Returns
        -------
        float:
            the value of the potential at the trial point.

        """

        # construct matrix of lattice vector combinations
        # (this could be extended to other lattices by modifiying the
        # matrix from the identity to a different basis).
        images = (np.asarray(list(itertools.product([0, 1],
                                                    repeat=len(trial))))
                  @ np.identity(len(trial)))

        # construct matrix of image basin positions (M, n, d) for
        # M basins, n images and d dimensions
        pos_images = images[None, :, :] + basin_positions[:, None, :]

        # construct the (M, n, d) matrix of displacements to image basins
        pos_disps = pos_images[:, :, None] - trial

        # contract over spatial index to yield (M, n) distance matrix
        distances = np.linalg.norm(pos_disps, axis=-1)

        # minimise over image index to yield (M, ) array of minimum dists
        min_dists = np.min(distances, axis=1).flatten()

        # compute potential from each closest image
        basins = 0.5 * min_dists**2 - basin_depths

        # return minimum potential at chosen point across basins
        return np.min(basins)

    def run(self, model, parameters):
        """ Compute the potential at the requetsed trial point. If
        `model.locally_optimize` is True, then use SciPy to find the
        local minmimum corresponding to the trial point.

        Parameters
        ----------
        model: :obj:`EggboxPESDataSourceModel`
            the model containing the parameters of the PES.
        parameters: :obj:`list` of :obj:`DataValue`
            list of parameters passed as DataValue objects, that match
            the input slots of this instance.

        """
        x0 = [float(param.value) for param in parameters]
        if np.max(np.abs(x0)) > 1:
            raise RuntimeError('MCO trial outside of bounds [0, 1]: {}'
                               .format(x0))
        bounds = np.array([[0, 1]
                           for i in range(model.dimension)])
        model.trials.append(x0)

        if model.locally_optimize:
            result = scipy.optimize.minimize(
                self.evaluate_potential, x0,
                args=(model,),
                bounds=bounds)

            results = [DataValue(value=result.x[i],
                                 type=model.cuba_design_space_type)
                       for i in range(model.dimension)]
            results.append(DataValue(value=result.fun,
                                     type=model.cuba_potential_type))

            model.results.append(result.x)

        else:
            result = self.evaluate_potential(x0, model)
            results = [DataValue(value=x0[i],
                                 type=model.cuba_design_space_type)
                       for i in range(model.dimension)]
            results.append(DataValue(value=result,
                                     type=model.cuba_potential_type))

            model.results.append(x0)

        return results

    def slots(self, model):
        """ The input/output slots for this instance.

        The input slots consist of one float per dimension in the
        simulation. The output slots consist of one float per dimension,
        to store the output position (either the same as the trial, or
        the optimised value) plus the value of the potential at that
        position.

        Parameters
        ----------
        model: :obj:`EggboxPESDataSourceModel`
            the model containing the parameters of the PES.

        Returns
        -------
        A tuple containing a tuple for the input slots, and a tuple for
        the output slots.

        """
        return (
            #: 1 input slot per dimension
            tuple(Slot(type=model.cuba_design_space_type,
                       description='element {} of trial vector'.format(i))
                  for i in range(model.dimension)
                  ),
            #: 1 output slot per dimension + 1 for the value of the potential
            tuple([Slot(type=model.cuba_design_space_type,
                        description='element {} of result'.format(i))
                   for i in range(model.dimension)] +
                  [Slot(type=model.cuba_potential_type,
                        description='value of potential at miminum')]
                  )
        )
