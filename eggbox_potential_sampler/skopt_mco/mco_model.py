from traits.api import Enum
from force_bdss.api import BaseMCOModel, PositiveInt, NonNegativeInt


class ModelBasedOptimizationMCOModel(BaseMCOModel):
    num_trials = NonNegativeInt(
        5,
        label='Number of estimator trials'
    )
    num_random_trials = NonNegativeInt(
        10,
        label='Number of random trials'
    )
    evaluation_mode = Enum(
        ["Internal", "Subprocess"],
        label='Workflow evaluation mode',
        desc="Whether to execute each point in a new BDSS subprocess"
    )
    estimator = Enum(
        'GP',
        values={"Gaussian process": "GP",
                "Random forest": "RF",
                "Extra trees": "ET",
                "Gradient-boosed tree": "GBRT"},
        label='Model Estimator',
        desc="The estimator to use for the Bayesian search"
    )
