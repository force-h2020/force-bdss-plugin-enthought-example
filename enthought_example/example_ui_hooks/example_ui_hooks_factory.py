from force_bdss.api import BaseUIHooksFactory, factory_id
from .example_ui_hooks_manager import ExampleUIHooksManager


class ExampleUIHooksFactory(BaseUIHooksFactory):
    """The UI Hooks are a collection of methods of the UIHook manager.
    These methods are called on specific circumstances during the Workflow
    Manager (the UI)."""

    #: As described in the data source factory
    id = factory_id("enthought", "example_ui_hooks")

    #: The UI Hooks manager class to instantiate. For a more flexible
    #: initialization, you can reimplement the create_ui_hooks_manager
    #: instead.
    #: For example::
    #:
    #: def create_ui_hooks_manager(self):
    #:    return ExampleUIHooksManager(self)
    ui_hooks_manager_class = ExampleUIHooksManager
