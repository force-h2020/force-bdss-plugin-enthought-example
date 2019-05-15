from traits.api import BaseInt, Enum, Trait
from traitsui.api import EnumEditor, Item, View
from force_bdss.api import BaseMCOModel


class NonNegativeInt(BaseInt):
    """A non-negative integer trait."""

    info_text = 'a non-negative integer'

    default_value = 0

    def validate(self, object, name, value):
        int_value = super(NonNegativeInt, self).validate(object, name, value)

        if int_value >= 0:
            return int_value

        self.error(object, name, value)


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
    estimator = Trait(
        "GP",
        label='Model Estimator',
        desc="The estimator to use for the Bayesian search"
    )

    def traits_view(self):
        return View(
            [Item('num_trials'),
             Item('num_random_trials'),
             Item('evaluation_mode'),
             Item('estimator',
                  editor=EnumEditor(values={"GP": "Gaussian process",
                                            "RF": "Random forest",
                                            "ET": "Extra trees",
                                            "GBRT": "Gradient-boosed tree"}))]
        )
