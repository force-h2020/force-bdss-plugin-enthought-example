from force_bdss.api import BaseDataSourceFactory

from .example_data_source_model import ExampleDataSourceModel
from .example_data_source import ExampleDataSource


class ExampleDataSourceFactory(BaseDataSourceFactory):
    """This class provides factory methods to generate the
    relevant instances for the data source.
    You need a model and the data source itself, so it provides
    methods for both to be overridden."""

    #: This id is used to differentiate the specific data source
    #: factory.
    #: You are responsible for keeping the entry unique _across_
    #: all your plugins, present and future. You can use (and are strongly
    #: advised to do so) a uuid.
    def get_identifier(self):
        return "example_data_source"

    #: A readable name of the data source. This will be displayed on
    #: the UI. Choose something meaningful.
    def get_name(self):
        return "Example Data Source (Power Evaluator)"

    #: You can specify the model class here.
    def get_model_class(self):
        return ExampleDataSourceModel

    #: You can specify your Data Source here.
    def get_data_source_class(self):
        return ExampleDataSource
