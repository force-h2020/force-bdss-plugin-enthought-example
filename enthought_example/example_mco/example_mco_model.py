from force_bdss.api import BaseMCOModel


class ExampleMCOModel(BaseMCOModel):
    """This is the model of the MCO. This one specifically does not contain
    anything additionally, but you can envision configuration options
    associated to your MCO.

    Note that the base class carries the parameters, with their specific
    values (e.g. two range parameters, the first with value from 0 to 10,
    the second from 100 to 200)
    """
    pass
