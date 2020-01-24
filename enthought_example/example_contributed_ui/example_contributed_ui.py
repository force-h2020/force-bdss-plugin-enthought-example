from traits.api import Float, Int, Property, on_trait_change
from traitsui.api import Group, Heading, Item

from force_wfmanager.ui import ContributedUI

_ENTHOUGHT_PLUGIN_ID = "force.bdss.enthought.plugin.example.v0.factory"


class ExampleContributedUI(ContributedUI):
    #: Name for the UI in selection screen
    name = "Example Workflow"

    #: Description of the UI
    desc = (
        "A simplified UI which allows the selection of a range and exponent"
    )

    #: Traits for settings in the UI
    lower = Int(1)
    upper = Int(9)
    power = Float(3.0)
    initial_value = Property(Float, depends_on='lower,upper')

    def _workflow_data_default(self):
        return self.workflow_data_update()

    @on_trait_change('lower,upper,power')
    def workflow_data_update(self):
        wf_data = {
            "version": "1",
            "workflow": {
                "mco_model": self._mco_data(),
                "execution_layers": self._execution_layer_data(),
                "notification_listeners":  self._notification_listener_data()
            }
        }
        self.workflow_data = wf_data
        return wf_data

    def _get_initial_value(self):
        return (self.lower + self.upper) / 2.0

    def _workflow_group_default(self):
        workflow_group = Group(
            Heading("Power Example Settings"),
            Item("lower", label="Lower bound"),
            Item("upper", label="Upper bound"),
            Item("power", label="Exponent"),
        )
        return workflow_group

    def _mco_data(self):
        return {
            "id": '.'.join([_ENTHOUGHT_PLUGIN_ID, "example_mco"]),
            "model_data": {
                "parameters": [
                    {
                        "id": ".".join([
                            _ENTHOUGHT_PLUGIN_ID, "example_mco",
                            "parameter", "ranged"
                        ]),
                        "model_data": {
                            "lower_bound": self.lower,
                            "upper_bound": self.upper,
                            "initial_value": self.initial_value,
                            "name": "input_number",
                            "type": "number"
                        }
                    }
                ],
                "kpis": [
                    {"name": "input_number_sq", "objective": "MINIMISE"},
                    {"name": "input_number_8", "objective": "MAXIMISE"}
                ],
            }
        }

    def _execution_layer_data(self):
        return [
            [
                {
                    "id": ".".join([
                        _ENTHOUGHT_PLUGIN_ID, "example_data_source"
                    ]),
                    "model_data": {
                        "power": self.power,
                        "cuba_type_in": "number",
                        "cuba_type_out": "number_sq",
                        "input_slot_info": [
                            {
                                "source": "Environment",
                                "name": "input_number"
                            }
                        ],
                        "output_slot_info": [
                            {
                                "name": "input_number_sq"
                            }
                        ]
                    }
                }
            ],
            [
                {
                    "id": ".".join([
                        _ENTHOUGHT_PLUGIN_ID, "example_data_source"
                    ]),
                    "model_data": {
                        "power": 4.0,
                        "cuba_type_in": "number_sq",
                        "cuba_type_out": "number_8",
                        "input_slot_info": [
                            {
                                "source": "Environment",
                                "name": "input_number_sq"
                            }
                        ],
                        "output_slot_info": [
                            {
                                "name": "input_number_8"
                            }
                        ]
                    }
                }
            ]
        ]

    def _notification_listener_data(self):
        return [
                {
                    "id": ".".join([
                        _ENTHOUGHT_PLUGIN_ID, "example_notification_listener"
                        ]),
                    "model_data": {}
                }
            ]
