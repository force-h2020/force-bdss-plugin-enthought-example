from unittest import mock
import numpy as np
import matplotlib.pyplot as plt

from force_bdss.api import BaseDataSourceFactory, DataValue
from eggbox_potential_sampler.eggbox_pes_data_source.data_source import (
    EggboxPESDataSource)
from eggbox_potential_sampler.eggbox_pes_data_source.model import (
    EggboxPESDataSourceModel)


def plot_potentials(sigmas=[0, 0.001, 0.01, 0.1, 1]):
    """ Plot and optimise potentials over a range of sigma values. """
    factory = mock.Mock(spec=BaseDataSourceFactory)
    for sigma in sigmas:
        ds = EggboxPESDataSource(factory)
        model = EggboxPESDataSourceModel(factory,
                                         num_cells=10,
                                         dimension=2,
                                         sigma_star=sigma)
        print(sigma)
        sample(1000, ds, model)
        plot_surface_to_file(ds, model)


def sample(n, ds, model):
    i = 0
    while i < n:
        random = np.random.rand(2)
        mock_params = [DataValue(value=random[0], type="float"),
                       DataValue(value=random[1], type="float")]
        ds.run(model, mock_params)
        i += 1


def plot_surface_to_file(data_source, model):
    if model.dimension == 1:
        x = np.linspace(0, 1, 512)
        z = np.zeros_like(x)
        x = x.reshape(len(x), 1)
        for ind, trial in enumerate(x):
            z[ind] = EggboxPESDataSource.evaluate_potential(trial, data_source)

        fig = plt.figure()
        ax = fig.add_subplot(111)

        ax.plot(x, z, alpha=0.8, lw=1, label='z')

        trials = np.asarray(data_source.trials).flatten()
        results = np.asarray(data_source.results).flatten()
        if len(trials) > 1 and len(results) > 1:
            trial_inds = (trials / (x[-1] / (len(x) - 1))).astype(int)
            results_inds = (results / (x[-1] / (len(x) - 1))).astype(int)
            z_trials = z[trial_inds]
            z_result = z[results_inds]
            ax.set_xlim(0, 1)
            ax.plot([trials, results], [z_trials, z_result],
                    lw=0.2, c='k', alpha=0.5)

        plt.savefig('1d_{}.png'.format(len(data_source.results)))

    elif model.dimension == 2:

        x = np.linspace(0, 1, 256)
        xx, yy = np.meshgrid(x, x)

        z = np.zeros((len(x), len(x)))
        evaluate_potential = EggboxPESDataSource.evaluate_potential
        for ind, _ in enumerate(xx):
            for jnd, _ in enumerate(yy):
                trial = np.asarray([xx[ind][jnd], yy[ind][jnd]])
                z[ind, jnd] = evaluate_potential(trial, model)

        trials = np.asarray(model.trials)
        results = np.asarray(model.results)

        fig = plt.figure(figsize=(4, 4))
        ax1 = fig.add_subplot(111, aspect='equal')
        im = ax1.pcolormesh(xx, yy, z)
        plt.colorbar(im, label='$V(x,y)$ (arb.)', ticks=[])
        ax1.set_title('$\\sigma^* = {}$'.format(model.sigma_star))
        ax1.set_xlabel('$x$')
        ax1.set_ylabel('$y$')
        ax1.set_yticklabels([])
        ax1.set_xticklabels([])
        ax1.plot([trials[:, 0], results[:, 0]], [trials[:, 1], results[:, 1]],
                 lw=0.2, c='k', alpha=0.5)
        plt.tight_layout()
        plt.savefig('pot_2d_{}.png'.format(model.sigma_star))


if __name__ == '__main__':
    plot_potentials()
