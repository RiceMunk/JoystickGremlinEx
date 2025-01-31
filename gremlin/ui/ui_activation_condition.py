# -*- coding: utf-8; -*-

# Based on original work by (C) Lionel Ott -  (C) EMCS 2024 and other contributors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from PySide6 import QtCore, QtGui, QtWidgets

import logging
from gremlin.input_types import InputType
from gremlin import hints, input_devices, macro, util
from gremlin.util import load_icon
import gremlin.base_classes as bc
from . import ui_common
from gremlin.base_conditions import *
import gremlin.keyboard


class ActivationConditionWidget(QtWidgets.QWidget):

    """Widget displaying the UI used to configure activation conditions."""

    # Signal which is emitted whenever the widget's contents change
    activation_condition_modified = QtCore.Signal()

    locked = False

    # Maps activation type name to index
    activation_type_to_index = {
        None: 0,
        "action": 1,
        "container": 2
    }

    def __init__(self, profile_data, parent=None):
        """Creates a new instance.

        :param profile_data the profile data associated with the conditions
        :param parent the parent widget of this
        """
        super().__init__(parent)
        self.profile_data = profile_data
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self._create_ui()

    def _create_ui(self):
        """Creates the configuration UI."""

        if ActivationConditionWidget.locked:
            return

        try:
            ActivationConditionWidget.locked = True
            self.granularity_selector = ui_common.QComboBox()
            self.granularity_selector.addItem("None")
            self.granularity_selector.addItem("Action")
            self.granularity_selector.addItem("Container")
            self.granularity_selector.setCurrentIndex(
                ActivationConditionWidget.activation_type_to_index[
                    self.profile_data.activation_condition_type
                ]
            )
            self.granularity_selector.currentIndexChanged.connect(
                self._granularity_changed_cb
            )

            self.help_button = QtWidgets.QPushButton(load_icon("gfx/help.png"), "")
            self.help_button.clicked.connect(self._show_hint)

            self.controls_layout = QtWidgets.QHBoxLayout()
            self.controls_layout.addWidget(QtWidgets.QLabel("Apply conditions to"))
            self.controls_layout.addWidget(self.granularity_selector)
            self.controls_layout.addWidget(self.help_button)

            self.controls_layout.addStretch()

            self.main_layout.addLayout(self.controls_layout)
            if self.profile_data.activation_condition_type == "container":
                self.condition_model = ConditionModel(
                    self.profile_data.activation_condition
                )
                self.condition_view = ConditionView()
                self.condition_view.set_model(self.condition_model)
                self.condition_view.redraw()

                self.main_layout.addWidget(self.condition_view)

            self.main_layout.addStretch()
        finally:
            ActivationConditionWidget.locked = False

    def _granularity_changed_cb(self, index):
        """Updates whether conditions are on actions or containers.

        :param index the entry of the selection box
        """
        from gremlin.base_classes import ActivationCondition, ActivationRule
        index_to_type = {
            0: None,
            1: "action",
            2: "container"
        }
        self.profile_data.activation_condition_type = index_to_type[index]

        if self.profile_data.activation_condition_type == "container":
            self.profile_data.activation_condition = \
                ActivationCondition(
                    [],
                    ActivationRule.All
                )
        else:
            self.profile_data.activation_condition = None

        self.activation_condition_modified.emit()

    def _show_hint(self, state):
        """Shows a help message.

        :param state push button state
        """
        QtWidgets.QWhatsThis.showText(
            self.help_button.mapToGlobal(QtCore.QPoint(0, 10)),
            hints.hint.get("cond:granularity", "")
        )


class AbstractConditionWidget(QtWidgets.QGroupBox):

    """Abstract class for condition ui widgets."""

    # Signal emitted when a condition is deleted
    #deleted = QtCore.Signal(base_classes.AbstractCondition)
    deleted = QtCore.Signal(object)

    def __init__(self, condition_data, parent=None):
        """Creates a new widget.

        :param condition_data the data to be represented by the widget
        :param parent the parent of this widget
        """
        super().__init__(parent)
        self.condition_data = condition_data

        self.main_layout = QtWidgets.QGridLayout(self)
        self.main_layout.setColumnMinimumWidth(0, 75)
        self.main_layout.setColumnMinimumWidth(1, 150)
        self.main_layout.setColumnMinimumWidth(2, 20)
        self.main_layout.setColumnStretch(3, 1)
        self._create_ui()

    def _create_ui(self):
        """Creates the configuration UI for this widget."""
        pass


class KeyboardConditionWidget(AbstractConditionWidget):

    """Widget allowing the configuration of a keyboard based condition."""

    locked = False

    def __init__(self, condition_data, parent=None):
        """Creates a new widget.

        :param condition_data the data to be represented by the widget
        :param parent the parent of this widget
        """
        super().__init__(condition_data, parent)
        self.setTitle("Keyboard Condition")

    def _create_ui(self):
        """Creates the configuration UI for this widget."""
        if KeyboardConditionWidget.locked:
            return
        
        try:
            KeyboardConditionWidget.locked = True

            self.key_label = QtWidgets.QLabel("")
            if self.condition_data.input_item:
                self.key_label.setText(f"<b>{self.condition_data.input_item.display_name}</b>")
            # if self.condition_data.scan_code is not None:
            #     self.key_label.setText(
            #         f"<b>{macro.key_from_code(
            #             self.condition_data.scan_code,
            #             self.condition_data.is_extended
            #         ).name}</b>"
            #         )
            self.record_button = ui_common.NoKeyboardPushButton(
                load_icon("gfx/button_edit.png"), ""
            )
            self.record_button.clicked.connect(self._request_user_input)
            self.delete_button = QtWidgets.QPushButton(
                load_icon("gfx/button_delete.png"), ""
            )
            self.delete_button.clicked.connect(
                lambda: self.deleted.emit(self.condition_data)
            )

            self.comparison_dropdown = ui_common.QComboBox()
            self.comparison_dropdown.addItem("Pressed")
            self.comparison_dropdown.addItem("Released")
            if self.condition_data.comparison:
                self.comparison_dropdown.setCurrentText(
                    self.condition_data.comparison.capitalize()
                )
            self.comparison_dropdown.currentTextChanged.connect(
                self._comparison_changed_cb
            )

            self.main_layout.addWidget(QtWidgets.QLabel("Activate if"), 0, 0)
            self.main_layout.addWidget(self.key_label, 0, 1)
            self.main_layout.addWidget(QtWidgets.QLabel("is"), 0, 2)
            self.main_layout.addWidget(
                self.comparison_dropdown, 0, 3, alignment=QtCore.Qt.AlignLeft
            )
            self.main_layout.addWidget(self.record_button, 0, 4)
            self.main_layout.addWidget(self.delete_button, 0, 5)
        finally:
            KeyboardConditionWidget.locked = False

    def _key_pressed_cb(self, key):
        """Updates the UI and model with the newly pressed key information.

        :param key the key that has been pressed
        """
        from gremlin.ui.keyboard_device import KeyboardInputItem
        input_item = KeyboardInputItem()
        input_item.key = key
        self.condition_data.input_item = input_item
        self.condition_data.scan_code = key.scan_code
        self.condition_data.is_extended = key.is_extended
        self.condition_data.comparison = \
            self.comparison_dropdown.currentText().lower()
        self.key_label.setText(f"<b>{input_item.display_name}</b>")

    def _comparison_changed_cb(self, text):
        """Updates the comparison operation to use.

        :param text the new comparison operation name
        """
        self.condition_data.comparison = text.lower()

    def _request_user_input(self):
        """Prompts the user for the input to bind to this item."""

        from gremlin.ui.virtual_keyboard import InputKeyboardDialog
        sequence = []
        if self.condition_data.input_item:
            sequence = self.condition_data.input_item.sequence
        self._keyboard_dialog = InputKeyboardDialog(sequence = sequence, parent = self, select_single = False, index = -1)
        self._keyboard_dialog.setModal(True)
        self._keyboard_dialog.accepted.connect(self._dialog_ok_cb)
        self._keyboard_dialog.showNormal()  

    def _dialog_ok_cb(self):
        ''' callled when the dialog completes '''

        # grab a new data index as this is a new entry
        self._key_pressed_cb(self._keyboard_dialog.latched_key)

        


class JoystickConditionWidget(AbstractConditionWidget):

    """Widget allowing the configuration of a joystick based condition."""

    locked = False

    def __init__(self, condition_data, parent=None):
        """Creates a new widget.

        :param condition_data the data to be represented by the widget
        :param parent the parent of this widget
        """
        self.input_event = None
        super().__init__(condition_data, parent)
        self.setTitle("Joystick Condition")

    def _create_ui(self):
        """Creates the configuration UI for this widget."""


        if JoystickConditionWidget.locked:
            return
        
        try:

            JoystickConditionWidget.locked = True

            ui_common.clear_layout(self.main_layout)

            self.record_button = QtWidgets.QPushButton(
                load_icon("gfx/button_edit.png"), ""
            )
            self.record_button.clicked.connect(self._request_user_input)
            self.delete_button = QtWidgets.QPushButton(
                load_icon("gfx/button_delete.png"), "")
            
            self.delete_button.clicked.connect(
                lambda: self.deleted.emit(self.condition_data)
            )

            self.main_layout.addWidget(QtWidgets.QLabel("Activate if"), 0, 0)
            if self.condition_data.input_type == InputType.JoystickAxis:
                self._axis_ui()
            elif self.condition_data.input_type == InputType.JoystickButton:
                self._button_ui()
            elif self.condition_data.input_type == InputType.JoystickHat:
                self._hat_ui()
            self.main_layout.addWidget(self.record_button, 0, 4)
            self.main_layout.addWidget(self.delete_button, 0, 5)
        finally:
            JoystickConditionWidget.locked = False

    def _axis_ui(self):
        """Creates the UI needed to configure an axis based condition."""
        self.lower = ui_common.DynamicDoubleSpinBox()
        self.lower.setMinimum(-1.0)
        self.lower.setMaximum(1.0)
        self.lower.setSingleStep(0.05)
        self.lower.setDecimals(3)
        self.lower.setValue(self.condition_data.range[0])
        self.lower.valueChanged.connect(self._range_lower_changed_cb)
        self.upper = ui_common.DynamicDoubleSpinBox()
        self.upper.setMinimum(-1.0)
        self.upper.setMaximum(1.0)
        self.upper.setDecimals(3)
        self.upper.setSingleStep(0.05)
        self.upper.setValue(self.condition_data.range[1])
        self.upper.valueChanged.connect(self._range_upper_changed_cb)

        self.comparison_dropdown = ui_common.QComboBox()
        self.comparison_dropdown.addItem("Inside")
        self.comparison_dropdown.addItem("Outside")
        self.comparison_dropdown.setCurrentText(
            self.condition_data.comparison.capitalize()
        )
        self.comparison_dropdown.currentTextChanged.connect(
            self._comparison_changed_cb
        )

        range_layout = QtWidgets.QHBoxLayout()
        range_layout.addWidget(self.comparison_dropdown)
        range_layout.addWidget(self.lower)
        range_layout.addWidget(QtWidgets.QLabel("and"))
        range_layout.addWidget(self.upper)

        input_label = QtWidgets.QLabel(
            f"<b>{self.condition_data.device_name} Axis {self.condition_data.input_id:d}</b>"
            )
        input_label.setWordWrap(True)
        self.main_layout.addWidget(input_label, 0, 1)
        self.main_layout.addWidget(QtWidgets.QLabel("is"), 0, 2)
        self.main_layout.addLayout(
            range_layout, 0, 3, alignment=QtCore.Qt.AlignLeft
        )

    def _button_ui(self):
        """Creates the UI needed to configure a button based condition."""
        self.comparison_dropdown = ui_common.QComboBox()
        self.comparison_dropdown.addItem("Pressed")
        self.comparison_dropdown.addItem("Released")
        self.comparison_dropdown.setCurrentText(
            self.condition_data.comparison.capitalize()
        )
        self.comparison_dropdown.currentTextChanged.connect(
            self._comparison_changed_cb
        )

        self.main_layout.addWidget(
            QtWidgets.QLabel(
                f"<b>{self.condition_data.device_name} Button {self.condition_data.input_id:d}</b>"
                ),
            0,
            1
        )
        self.main_layout.addWidget(QtWidgets.QLabel("is"), 0, 2)
        self.main_layout.addWidget(
            self.comparison_dropdown, 0, 3, alignment=QtCore.Qt.AlignLeft
        )

    def _hat_ui(self):
        """Creates the UI needed to configure a hat based condition."""
        directions = [
            "Center", "North", "North East", "East", "South East",
            "South", "South West", "West", "North West"
        ]
        self.comparison_dropdown = ui_common.QComboBox()
        for entry in directions:
            self.comparison_dropdown.addItem(entry)
        self.comparison_dropdown.setCurrentText(
            self.condition_data.comparison.replace("-", " ").title()
        )
        self.comparison_dropdown.currentTextChanged.connect(
            self._comparison_changed_cb
        )

        self.main_layout.addWidget(
            QtWidgets.QLabel(
                f"<b>{self.condition_data.device_name} Hat {self.condition_data.input_id:d}</b>"
                ),
            0,
            1
        )
        self.main_layout.addWidget(QtWidgets.QLabel("is"), 0, 2)
        self.main_layout.addWidget(
            self.comparison_dropdown, 0, 3, alignment=QtCore.Qt.AlignLeft
        )

    def _input_pressed_cb(self, event):
        """Processes input events to update the UI and model.

        :param event the input event to process
        """
        self.condition_data.device_guid = event.device_guid
        self.condition_data.input_type = event.event_type
        self.condition_data.input_id = event.identifier
        self.condition_data.device_name = \
            input_devices.JoystickProxy()[event.device_guid].name
        if event.event_type == InputType.JoystickAxis:
            self.condition_data.comparison = "inside"
        elif event.event_type == InputType.JoystickButton:
            self.condition_data.comparison = "pressed"
        elif event.event_type == InputType.JoystickHat:
            self.condition_data.comparison = \
                util.hat_tuple_to_direction(event.value)
        self._create_ui()

    def _request_user_input(self):
        """Prompts the user for the input to bind to this item."""
        self.input_dialog = ui_common.InputListenerWidget(
            [
                InputType.JoystickAxis,
                InputType.JoystickButton,
                InputType.JoystickHat
            ],
            return_kb_event=False,
            multi_keys=False
        )
        self.input_dialog.item_selected.connect(self._input_pressed_cb)

        # Display the dialog centered in the middle of the UI
        root = self
        while root.parent():
            root = root.parent()
        geom = root.geometry()

        self.input_dialog.setGeometry(
            int(geom.x() + geom.width() / 2 - 150),
            int(geom.y() + geom.height() / 2 - 75),
            300,
            150
        )
        self.input_dialog.show()

    def _range_lower_changed_cb(self, value):
        """Updates the lower part of an axis range.

        :param value the new value
        """
        self.condition_data.range[0] = value

    def _range_upper_changed_cb(self, value):
        """Updates the upper part of an axis range.

        :param value the new value
        """
        self.condition_data.range[1] = value

    def _comparison_changed_cb(self, text):
        """Updates the comparison operation to use.

        :param text the new comparison operation name
        """
        if self.condition_data.input_type == InputType.JoystickButton:
            self.condition_data.comparison = text.lower()
        elif self.condition_data.input_type == InputType.JoystickHat:
            self.condition_data.comparison = text.replace(" ", "-").lower()
        elif self.condition_data.input_type == InputType.JoystickAxis:
            self.condition_data.comparison = text.lower()
        else:
            logging.getLogger("system").warning(
                f"Invalid input type encountered: {self.condition_data.input_type}"
            )


class VJoyConditionWidget(AbstractConditionWidget):

    """Widget allowing the configuration of a vJoy based condition."""

    locked = False

    def __init__(self, condition_data, parent=None):
        """Creates a new widget.

        Parameters
        ==========
        condition_data : VJoyCondition
            data to be represented by the widget
        parent : QObject
            parent of this widget
        """
        self.input_event = None
        super().__init__(condition_data, parent)
        self.setTitle("vJoy Condition")

        # Initialize UI fully
        self._modify_vjoy(self.vjoy_selector.get_selection())


    def _create_ui(self):
        """Creates the configuration UI for this widget."""
        if VJoyConditionWidget.locked:
            return
        
        VJoyConditionWidget.locked = True
        
        try:

            ui_common.clear_layout(self.main_layout)

            self.vjoy_selector = ui_common.VJoySelector(
                self._modify_vjoy,
                [
                    InputType.JoystickAxis,
                    InputType.JoystickButton,
                    InputType.JoystickHat
                ]
            )
            self.vjoy_selector.set_selection(
                self.condition_data.input_type,
                self.condition_data.vjoy_id,
                self.condition_data.input_id
            )
            self.delete_button = QtWidgets.QPushButton(
                load_icon("gfx/button_delete.png"), "")
            self.delete_button.clicked.connect(
                lambda: self.deleted.emit(self.condition_data)
            )

            self.main_layout.addWidget(QtWidgets.QLabel("Activate if"), 0, 0)
            if self.condition_data.input_type == InputType.JoystickAxis:
                self._axis_ui()
            elif self.condition_data.input_type == InputType.JoystickButton:
                self._button_ui()
            elif self.condition_data.input_type == InputType.JoystickHat:
                self._hat_ui()
            self.main_layout.addWidget(self.vjoy_selector, 0, 4)
            self.main_layout.addWidget(self.delete_button, 0, 5)

        finally:
            VJoyConditionWidget.locked = False

    def _axis_ui(self):
        """Creates the UI needed to configure an axis based condition."""
        self.lower = ui_common.DynamicDoubleSpinBox()
        self.lower.setMinimum(-1.0)
        self.lower.setMaximum(1.0)
        self.lower.setSingleStep(0.05)
        self.lower.setDecimals(3)
        self.lower.setValue(self.condition_data.range[0])
        self.lower.valueChanged.connect(self._range_lower_changed_cb)
        self.upper = ui_common.DynamicDoubleSpinBox()
        self.upper.setMinimum(-1.0)
        self.upper.setMaximum(1.0)
        self.upper.setDecimals(3)
        self.upper.setSingleStep(0.05)
        self.upper.setValue(self.condition_data.range[1])
        self.upper.valueChanged.connect(self._range_upper_changed_cb)

        self.comparison_dropdown = ui_common.QComboBox()
        self.comparison_dropdown.addItem("Inside")
        self.comparison_dropdown.addItem("Outside")
        self.comparison_dropdown.setCurrentText(
            self.condition_data.comparison.capitalize()
        )
        self.comparison_dropdown.currentTextChanged.connect(
            self._comparison_changed_cb
        )

        range_layout = QtWidgets.QHBoxLayout()
        range_layout.addWidget(self.comparison_dropdown)
        range_layout.addWidget(self.lower)
        range_layout.addWidget(QtWidgets.QLabel("and"))
        range_layout.addWidget(self.upper)

        input_label = QtWidgets.QLabel(
            f"<b>vJoy {self.condition_data.vjoy_id:d} Axis {self.condition_data.input_id:d}</b>"
            )
        input_label.setWordWrap(True)
        self.main_layout.addWidget(input_label, 0, 1)
        self.main_layout.addWidget(QtWidgets.QLabel("is"), 0, 2)
        self.main_layout.addLayout(
            range_layout, 0, 3, alignment=QtCore.Qt.AlignLeft
        )

    def _button_ui(self):
        """Creates the UI needed to configure a button based condition."""
        self.comparison_dropdown = ui_common.QComboBox()
        self.comparison_dropdown.addItem("Pressed")
        self.comparison_dropdown.addItem("Released")
        self.comparison_dropdown.setCurrentText(
            self.condition_data.comparison.capitalize()
        )
        self.comparison_dropdown.currentTextChanged.connect(
            self._comparison_changed_cb
        )

        self.main_layout.addWidget(
            QtWidgets.QLabel(
                f"<b>vJoy {self.condition_data.vjoy_id:d} Button {self.condition_data.input_id:d}</b>"
                ),
            0,
            1
        )
        self.main_layout.addWidget(QtWidgets.QLabel("is"), 0, 2)
        self.main_layout.addWidget(
            self.comparison_dropdown, 0, 3, alignment=QtCore.Qt.AlignLeft
        )

    def _hat_ui(self):
        """Creates the UI needed to configure a hat based condition."""
        directions = [
            "Center", "North", "North East", "East", "South East",
            "South", "South West", "West", "North West"
        ]
        self.comparison_dropdown = ui_common.QComboBox()
        for entry in directions:
            self.comparison_dropdown.addItem(entry)
        self.comparison_dropdown.setCurrentText(
            self.condition_data.comparison.replace("-", " ").title()
        )
        self.comparison_dropdown.currentTextChanged.connect(
            self._comparison_changed_cb
        )

        self.main_layout.addWidget(
            QtWidgets.QLabel(
                f"<b>vJoy {self.condition_data.vjoy_id:d} Hat {self.condition_data.input_id:d}</b>"
                ),
            0,
            1
        )
        self.main_layout.addWidget(QtWidgets.QLabel("is"), 0, 2)
        self.main_layout.addWidget(
            self.comparison_dropdown, 0, 3, alignment=QtCore.Qt.AlignLeft
        )

    def _modify_vjoy(self, data):
        # fix: 5/29/24 EMCS don't override prior value if already a valid value to prevent a condition reset
        self.condition_data.vjoy_id = data["device_id"]
        self.condition_data.input_type = data["input_type"]
        self.condition_data.input_id = data["input_id"]

        if data["input_type"] == InputType.JoystickAxis:
            if not self.condition_data.comparison in ("inside","outside"):
                self.condition_data.comparison = "inside"
        elif data["input_type"] == InputType.JoystickButton:
            if not self.condition_data.comparison in ("pressed","released"):
                self.condition_data.comparison = "pressed"
        elif data["input_type"] == InputType.JoystickHat:
            directions = ("center", "north", "north-east", "east", "south-east","south", "south-west", "west", "north-west")
            if not self.condition_data.comparison in directions:
                self.condition_data.comparison = util.hat_tuple_to_direction((0, 0))
        self._create_ui()

    def _range_lower_changed_cb(self, value):
        """Updates the lower part of an axis range.

        :param value the new value
        """
        self.condition_data.range[0] = value

    def _range_upper_changed_cb(self, value):
        """Updates the upper part of an axis range.

        :param value the new value
        """
        self.condition_data.range[1] = value

    def _comparison_changed_cb(self, text):
        """Updates the comparison operation to use.

        :param text the new comparison operation name
        """
        if self.condition_data.input_type == InputType.JoystickButton:
            self.condition_data.comparison = text.lower()
        elif self.condition_data.input_type == InputType.JoystickHat:
            self.condition_data.comparison = text.replace(" ", "-").lower()
        elif self.condition_data.input_type == InputType.JoystickAxis:
            self.condition_data.comparison = text.lower()
        else:
            logging.getLogger("system").warning(
                f"Invalid input type encountered: {self.condition_data.input_type}"
            )


class InputActionConditionWidget(AbstractConditionWidget):

    """Creates the UI needed to configure an input action based condition."""

    locked = False

    def __init__(self, condition_data, parent=None):
        """Creates a new widget.

        :param condition_data the data to be represented by the widget
        :param parent the parent of this widget
        """
        super().__init__(condition_data, parent)
        self.setTitle("Action Condition")

    def _create_ui(self):
        """Creates the configuration UI for this widget."""

        if InputActionConditionWidget.locked:
            return

        try:
            InputActionConditionWidget.locked = True

            self.state_dropdown = ui_common.QComboBox()
            self.state_dropdown.addItem("Pressed")
            self.state_dropdown.addItem("Released")
            if self.condition_data.comparison:
                self.state_dropdown.setCurrentText(
                    self.condition_data.comparison.capitalize()
                )
            else:
                self.condition_data.comparison = "pressed"
            self.state_dropdown.currentTextChanged.connect(
                self._state_selection_changed
            )
            self.delete_button = QtWidgets.QPushButton(
                load_icon("gfx/button_delete.png"), "")
            
            self.delete_button.clicked.connect(
                lambda: self.deleted.emit(self.condition_data)
            )

            self.main_layout.addWidget(QtWidgets.QLabel("Activate when"), 0, 0)
            self.main_layout.addWidget(
                QtWidgets.QLabel("<b>this (virtual) button</b>"),
                0,
                1
            )
            self.main_layout.addWidget(QtWidgets.QLabel("is"), 0, 2)
            self.main_layout.addWidget(
                self.state_dropdown, 0, 3, alignment=QtCore.Qt.AlignLeft
            )
            self.main_layout.addWidget(self.delete_button, 0, 5)
        finally:
            InputActionConditionWidget.locked = False

    def _state_selection_changed(self, label):
        """Updates the activation state of the condition.

        :param label the new activation state
        """
        self.condition_data.comparison = label.lower()


class ConditionModel(ui_common.AbstractModel):

    """Stores and represents condition data."""

    def __init__(self, condition_data, parent=None):
        """Creates a new model to store condition data.

        :param condition_data the condition data to represent
        :param parent the parent of this object
        """
        super().__init__(parent)
        self.condition_data = condition_data

    def rows(self):
        """Returns the number of rows in the model.

        :return number of rows
        """
        return len(self.condition_data.conditions)

    def data(self, index):
        """Returns the data stored at the given index.

        :param index the index for which to return the data
        :return the data stored at the provided index
        """
        return self.condition_data.conditions[index]

    def add_condition(self, condition_data):
        """Adds a condition to to the model.

        :param condition_data the condition data to add
        """
        self.condition_data.conditions.append(condition_data)
        self.data_changed.emit()

    def delete_condition(self, condition_data):
        """Deletes a condition from the model.

        Attempts to locate the provided condition and deletes it, if it is
        present.

        :param condition_data the condition to remove.
        """
        idx = self.condition_data.conditions.index(condition_data)
        if idx != -1:
            del self.condition_data.conditions[idx]
        self.data_changed.emit()

    @property
    def rule(self):
        """Returns the current application rule for the conditions.

        :return current application rule of conditions
        """
        return self.condition_data.rule

    @rule.setter
    def rule(self, rule):
        """Sets the application rule of the conditions.

        :param rule the new application type
        """
        self.condition_data.rule = rule


class ConditionView(ui_common.AbstractView):

    """Widget visualizing a condition model instance."""

    # Mapping between data and ui classes
    
    
    condition_map = {
        "Keyboard":
            [KeyboardCondition, KeyboardConditionWidget],
        "Joystick":
            [JoystickCondition, JoystickConditionWidget],
        "vJoy":
            [VJoyCondition, VJoyConditionWidget],
        "Action":
            [InputActionCondition, InputActionConditionWidget]
    }

    # Mapping between application rule label and enumeration
    rules_map = {
        "All": ActivationRule.All,
        "Any": ActivationRule.Any,
        ActivationRule.All: "All",
        ActivationRule.Any: "Any"
    }

    def __init__(self, parent=None):
        """Creates a new instance.

        :param parent the parent of this widget
        """
        super().__init__(parent)

        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.controls_layout = QtWidgets.QHBoxLayout()
        self.conditions_layout = QtWidgets.QVBoxLayout()

        self.main_layout.addLayout(self.controls_layout)
        self.main_layout.addLayout(self.conditions_layout)

        # Condition truth rules
        self.rule_selector = ui_common.QComboBox()
        self.rule_selector.addItem("All")
        self.rule_selector.addItem("Any")
        self.rule_selector.currentTextChanged.connect(self._rule_changed_cb)
        self.controls_layout.addWidget(QtWidgets.QLabel("Requires "))
        self.controls_layout.addWidget(self.rule_selector)
        self.controls_layout.addWidget(
            QtWidgets.QLabel("condition(s) to be met")
        )

        self.controls_layout.addStretch()

        # Condition selector
        self.condition_selector = ui_common.QComboBox()
        self.condition_selector.addItem("Keyboard Condition")
        self.condition_selector.addItem("Joystick Condition")
        self.condition_selector.addItem("vJoy Condition")
        self.condition_selector.addItem("Action Condition")
        self.condition_add_button = QtWidgets.QPushButton("Add")
        self.condition_add_button.clicked.connect(self._add_condition)
        self.controls_layout.addWidget(self.condition_selector)
        self.controls_layout.addWidget(self.condition_add_button)

        self.help_button = QtWidgets.QPushButton(load_icon("gfx/help.png"), "")
        self.help_button.clicked.connect(self._show_hint)
        self.controls_layout.addWidget(self.help_button)

    def redraw(self):
        """Redraws the entire view."""
        ui_common.clear_layout(self.conditions_layout)

        lookup = {}
        for entry in ConditionView.condition_map.values():
            lookup[entry[0]] = entry[1]

        for i in range(self.model.rows()):
            data = self.model.data(i)
            condition_widget = lookup[type(data)](data)
            condition_widget.deleted.connect(
                lambda local_data: self.model.delete_condition(local_data)
            )
            self.conditions_layout.addWidget(condition_widget)

    def _add_condition(self):
        """Adds a condition to the view's model."""
        data_type = ConditionView.condition_map[
            self.condition_selector.currentText().split()[0]
        ][0]
        self.model.add_condition(data_type())

    def _rule_changed_cb(self, text):
        """Updates the rule of the model.

        :param text the new rule value
        """
        self.model.rule = ConditionView.rules_map[text]

    def _model_changed(self):
        """Updates the view when the model changes."""
        self.rule_selector.setCurrentText(
            ConditionView.rules_map[self.model.rule]
        )

    def _show_hint(self, state):
        """Shows a help message regarding the condition types.

        :param state push button state
        """
        QtWidgets.QWhatsThis.showText(
            self.help_button.mapToGlobal(QtCore.QPoint(0, 10)),
            hints.hint.get("cond:types", "")
        )
