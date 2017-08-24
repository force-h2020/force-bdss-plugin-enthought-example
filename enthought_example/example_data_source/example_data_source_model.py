from traits.api import Float, String, on_trait_change

from force_bdss.api import BaseDataSourceModel


class ExampleDataSourceModel(BaseDataSourceModel):
    """This model contains the data that the data source
    needs to perform its work. It is information that is
    outside the pipeline system. Example of this information
    could be, for example, authentication data (login/password)
    to a database data source. They are configured when constructing
    your workflow and do not change as the workflow is computed.
    """

    #: In this data source, we specify the power factor default.
    #: It will appear in the UI as an appropriate UI control.
    #: The default is 1.0, meaning that the input data will be elevated to
    #: the power of one to produce the output data.
    power = Float(1.0)

    #: This is an example, still work in progess, of how to handle variable
    #: (customizable) CUBA types, that is, a source that can return a specified
    #: CBUA type.
    #: We assume that this data source accepts data having some CUBA type,
    #: and, potentially after transformation, generates the same or different
    #: CUBA type. In this case, the CUBA type is specified by the user.
    #: There are valid instances of this case. For example, if you have a data
    #: source extracting from a CSV file, there might be no information about
    #: the type in the file, but you know that it represents a pressure.
    cuba_type_in = String()
    cuba_type_out = String()

    #: Data sources inputs and outputs may change depending on
    #: the settings in the model. For example, you might have a configuration
    #: option that enables some functionality of your data source, and that
    #: might produce different data as result, or require different data as
    #: input. It is imperative that you observe the traits that may affect the
    #: resulting inputs and outputs, and report this fact performing as it is
    #: done here.
    #: Note: we might make this more streamlined in the future, so you might
    #: not need to define this method explicitly.
    #: For the time being, be aware that you should not put a space
    #: between individual trait names, so
    #:
    #: @on_trait_change("cuba_type_in, cuba_type_out")
    #:
    #: might give problems.
    @on_trait_change("cuba_type_in,cuba_type_out")
    def _notify_changes_slots(self):
        self.changes_slots = True
