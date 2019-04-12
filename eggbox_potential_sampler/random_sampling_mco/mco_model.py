from traits.api import Enum
from force_bdss.api import BaseMCOModel, PositiveInt


class RandomSamplingMCOModel(BaseMCOModel):
    num_trials = PositiveInt(5000,
                             label='Number of trials',
                             desc='The number of random trials to perform')
    evaluation_mode = Enum("Internal", "Subprocess")
