from force_bdss.api import BaseUIHooksFactory
from .example_ui_hooks_manager import ExampleUIHooksManager


class ExampleUIHooksFactory(BaseUIHooksFactory):
    """The UI Hooks are a collection of methods of the UIHook manager.
    These methods are called on specific circumstances during the Workflow
    Manager (the UI)."""

    #: Define this method to return the name of the factory. It must
    #: be unique within the context of your plugin.
    def get_identifier(self):
        return "example_ui_hooks"

    #: Define a user-visible, free form string for the factory
    def get_name(self):
        return "Example UI Hooks"

    #: The UI Hooks manager class to instantiate. Return the manager class.
    def get_ui_hooks_manager_class(self):
        return ExampleUIHooksManager
