from traits.api import Enum
from force_bdss.api import BaseMCOModel, PositiveInt


class ModelBasedOptimizationMCOModel(BaseMCOModel):
    num_trials = PositiveInt(5)
    evaluation_mode = Enum("Internal", "Subprocess")
