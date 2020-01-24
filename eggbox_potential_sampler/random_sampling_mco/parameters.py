from force_bdss.api import (
    BaseMCOParameter, BaseMCOParameterFactory
)


class DummyMCOParameter(BaseMCOParameter):
    """ Expresses a named MCO parameter with values set directly by the
    MCO.
    """


class DummyMCOParameterFactory(BaseMCOParameterFactory):
    """The factory of the above model"""
    def get_identifier(self):
        return "dummy"

    def get_name(self):
        return "Dummy"

    def get_model_class(self):
        return DummyMCOParameter

    def get_description(self):
        return "A named parameter with values to be set by the MCO."
