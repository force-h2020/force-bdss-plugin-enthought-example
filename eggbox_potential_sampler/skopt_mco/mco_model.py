from traits.api import Enum
from force_bdss.api import BaseMCOModel, PositiveInt, NonNegativeInt


class ModelBasedOptimizationMCOModel(BaseMCOModel):
    num_trials = PositiveInt(
        5,
        label='Number of estimator trials'
    )
    num_random_trials = NonNegativeInt(
        10,
        label='Number of initial random trials'
    )
    evaluation_mode = Enum(
        ["Internal", "Subprocess"],
        label='Workflow evaluation mode',
        desc="Whether to execute each point in a new BDSS subprocess"
    )
    estimator = Enum(
        ["GP", "RF", "ET", "GBRT"],
        label='Model Estimator',
        desc="The estimator to use for the Bayesian search"
    )
