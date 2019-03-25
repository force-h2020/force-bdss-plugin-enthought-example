from .eggbox_pes_data_source_model import EggboxPESDataSourceModel
from .eggbox_pes_data_source import EggboxPESDataSource


def plot_surface_to_file(data_source):
    import matplotlib.pyplot as plt
    import numpy as np
    if data_source.dimension == 1:
        x = np.linspace(-data_source.num_cells, data_source.num_cells, 512)
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
            trial_inds =   int((len(x) - 1) / 2) + (trials / (2 * x[-1] / (len(x) - 1))).astype(int)
            results_inds = int((len(x) - 1) / 2) + (results / (2 * x[-1] / (len(x) - 1))).astype(int)
            z_trials = z[trial_inds]
            z_result = z[results_inds]
            ax.set_xlim(-data_source.num_cells, data_source.num_cells)
            ax.plot([trials, results], [z_trials, z_result],
                    lw=0.2, c='k', alpha=0.5)

        plt.savefig('1d_{}.png'.format(len(data_source.results)))

    elif data_source.dimension == 2:

        x = np.linspace(-data_source.num_cells, data_source.num_cells, 128)
        xx, yy = np.meshgrid(x, x)

        z = np.zeros((len(x), len(x)))
        for ind, _ in enumerate(xx):
            for jnd, _ in enumerate(yy):
                trial = np.asarray([xx[ind][jnd], yy[ind][jnd]])
                z[ind, jnd] = EggboxPESDataSource.evaluate_potential(trial, data_source)

        trials = np.asarray(data_source.trials)
        results = np.asarray(data_source.results)

        fig = plt.figure(figsize=(10, 3))
        ax1 = fig.add_subplot(131, aspect='equal')
        im = ax1.pcolor(xx, yy, z)
        plt.colorbar(im)
        ax1.plot([trials[:, 0], results[:, 0]], [trials[:, 1], results[:, 1]], lw=0.2, c='k', alpha=0.5)
        ax2 = fig.add_subplot(132, aspect='equal')
        # ax2.scatter(trials[:, 0], trials[:, 1], c='red', s=2)
        ax2.scatter(results[:, 0], results[:, 1], c='k', s=2)
        ax3 = fig.add_subplot(133)
        ax3.plot(x, z[:, int(len(z)/2)])
        plt.savefig('pot_2d.png', dpi=300)
