from traits.api import Float

from force_bdss.api import (
    BaseMCOParameter,
    BaseMCOParameterFactory)


class RangedMCOParameter(BaseMCOParameter):
    """Expresses a MCO parameter that has a range between two floating
    point values."""
    initial_value = Float(0.0)
    lower_bound = Float(0.0)
    upper_bound = Float(1.0)


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
