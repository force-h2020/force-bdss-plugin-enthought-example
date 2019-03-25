from traits.api import Enum
from force_bdss.api import BaseMCOModel, PositiveInt


class RandomSamplingMCOModel(BaseMCOModel):
    num_trials = PositiveInt(5)
    evaluation_mode = Enum("Internal", "Subprocess")
