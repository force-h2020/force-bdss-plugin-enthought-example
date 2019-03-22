from traits.api import Bool, Float, Property, Range
from traitsui.api import TextEditor, View, Item

from force_bdss.api import BaseMCOParameter, BaseMCOParameterFactory




class RangedMCOParameter(BaseMCOParameter):
    """ Expresses a MCO parameter that has a range between two floating
    point values.

    """

    lower_bound = Property(Float)
    _lower_bound = Float(0.0)
    upper_bound = Property(Float)
    _upper_bound = Float(0.0)
    initial_value = Range(
        low="_lower_bound",
        high="_upper_bound",
        label="Initial value",
        depends_on="lower_bound,upper_bound",
    )


    def default_traits_view(self):
        return View(
            Item("lower_bound"),
            Item("upper_bound"),
            Item("initial_value")
        )

    def _set_lower_bound(self, val):
        if val <= self.upper_bound:
            self._lower_bound = val

        if self.initial_value < self.lower_bound:
            self.initial_value = (self.lower_bound + self.upper_bound) / 2.0

    def _set_upper_bound(self, val):
        if val >= self.lower_bound:
            self._upper_bound = val

        if self.initial_value > self.upper_bound:
            self.initial_value = (self.lower_bound + self.upper_bound) / 2.0

    def _get_lower_bound(self):
        return self._lower_bound

    def _get_upper_bound(self):
        return self._upper_bound

    # def valid(self):
    #     return self.lower_bound < self.initial_value < self.upper_bound


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
