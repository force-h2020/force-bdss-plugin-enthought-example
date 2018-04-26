from traits.api import String

from force_bdss.api import factory_id, BaseDataSourceFactory

from .example_data_source_model import ExampleDataSourceModel
from .example_data_source import ExampleDataSource


class ExampleDataSourceFactory(BaseDataSourceFactory):
    """This class provides factory methods to generate the
    relevant instances for the data source.
    You need a model and the data source itself, so it provides
    methods for both to be overridden."""

    #: This id is used to differentiate the specific data source
    #: factory. Note that you don't use plugin_id, but factory_id.
    #: Like in the case of the plugin id, the first entry is your
    #: organization unique name.
    #: You are responsible for keeping the second entry unique _across_
    #: all your plugins, present and future. You can use (and are strongly
    #: advised to do so) a uuid. In this case, it's just a readable string.
    id = String(factory_id("enthought", "example_data_source"))

    #: A readable name of the data source. This will be displayed on
    #: the UI. Choose something meaningful.
    name = String("Example Data Source (Power Evaluator)")

    #: You can specify the model class here. If you want to have a more complex
    #: model initialization, you can leave this variable unspecified, and
    #: override the create_model method instead.
    #: For example::
    #:
    #:     def create_model(self, model_data=None):
    #:         """Define this method to generate your model.
    #:         In general, this boilerplate is enough."""
    #:         if model_data is None:
    #:             model_data = {}
    #:
    #:         return ExampleDataSourceModel(self, **model_data)
    model_class = ExampleDataSourceModel

    #: You can specify your Data Source here. If you want to have a more
    #: complex initialization, you can reimplement the create_data_source
    #: method instead.
    #: For example::
    #:
    #:     def create_data_source(self):
    #:         """Return the Data Source instance."""
    #:         return ExampleDataSource(self)
    data_source_class = ExampleDataSource

