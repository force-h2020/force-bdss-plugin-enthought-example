#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

from force_bdss.api import BaseUIHooksManager


class ExampleUIHooksManager(BaseUIHooksManager):
    """The UIHookManager implements various methods that are called
    on a specific moment of the UI execution. The UI Task is passed, so
    you have pretty much full control over the UI application, including
    the workflow model.

    Each of these methods are optional in implementation, if you don't have
    any need to control the application during that phase. Simply implement
    only the methods you want.
    """

    def before_execution(self, task):
        print("This is the example UI hook. The execution is about to begin.")

    def after_execution(self, task):
        print("This is the example UI hook. The execution is done.")

    def before_save(self, task):
        print("This is the example UI hook. The save is about to begin.")
