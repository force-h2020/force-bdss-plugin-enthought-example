from traits.api import Float

from force_bdss.api import (
    mco_parameter_id,
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
    #: As in the case of the other ids, the first entry is the name
    #: of your organization.
    #: The second name should match the MCOFactory factory_id second argument.
    #: it must be kept unique throughout your extensions and you are fully
    #: responsible for having them as such. You can use a uuid if you want.
    #: The third entry must be unique for the parameter. Once again
    #: you are fully responsible for its uniqueness, but note that
    #: you can certainly have the same entry, provided that they
    #: differ in the second (that is, they belong to two different MCO
    #: extensions).
    #: In other words, if you provide support for two mcos: mco1 and mco2, the
    #: first can have a ranged parameter with id
    #:
    #:      mco_parameter_id("enthought", "mco1", "ranged")
    #:
    #: and the second can have
    #:
    #:      mco_parameter_id("enthought", "mco2", "ranged")
    #:
    #: without any conflict arising. You can also use different names for the
    #: third parameter as well. There is no mapping between parameters across
    #: MCOs. Again, you are free to choose a uuid if you so prefer.
    id = mco_parameter_id("enthought", "example_mco", "ranged")

    #: Definition of the associated model class is a bit more compact than
    #: in the case of the other factories we've seen until now. This pattern
    #: will eventually be used also in the other factories. You specify the
    #: model class to generate, which is the parameter class above, as a
    #: class variable.
    model_class = RangedMCOParameter

    #: A name that will appear in the UI to identify this parameter.
    name = "Range"

    #: and a long description
    description = "A ranged parameter in floating point values."
