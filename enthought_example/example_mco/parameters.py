from traits.api import Float, Range, on_trait_change
from traitsui.api import View, Item

from force_bdss.api import BaseMCOParameter, BaseMCOParameterFactory


class RangedMCOParameter(BaseMCOParameter):
    """ Expresses a MCO parameter that has a range between two floating
    point values.

    """
    range_start = Float(0.0)
    range_end = Float(0.0)
    lower_bound = Float
    upper_bound = Float

    initial_value = Range(
        low="lower_bound",
        high="upper_bound",
        label="Initial value",
        depends_on="lower_bound,upper_bound",
    )

    def default_traits_view(self):
        return View(
            Item("range_start"),
            Item("range_end"),
            Item("initial_value")
        )

    @on_trait_change("range_start,range_end")
    def set_bounds(self):
        self.lower_bound = min(self.range_start, self.range_end)
        self.upper_bound = max(self.range_start, self.range_end)
        if not self.lower_bound <= self.initial_value <= self.upper_bound:
            self.initial_value = (self.lower_bound + self.upper_bound) / 2.0

    def __init__(self, *args, **model_data):
        """ Custom init to prevent argument ordering issues after
        expansion; since the validity of `intial_value` is checked when
        it is set, the bounds need to be set first.

        """
        cached_initial_value = model_data.pop("initial_value", None)
        super(RangedMCOParameter, self).__init__(*args, **model_data)
        if cached_initial_value:
            self.initial_value = cached_initial_value


class RangedMCOParameterFactory(BaseMCOParameterFactory):
    """The factory of the above model"""

    #: This identifier must be unique for your parameter.
    #: Once again you are fully responsible for its uniqueness within the scope
    #: of the MCO it belongs to. You can have the same identifier if and only
    #: if they belong to different MCOs.
    #: Again, you are free to choose a uuid if you so prefer.
    def get_identifier(self):
        return "ranged"

    #: A name that will appear in the UI to identify this parameter.
    def get_name(self):
        return "Range"

    #: Definition of the associated model class.
    def get_model_class(self):
        return RangedMCOParameter

    #: A long description of the parameter
    def get_description(self):
        return "A ranged parameter in floating point values."
