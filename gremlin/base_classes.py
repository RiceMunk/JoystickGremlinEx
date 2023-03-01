# -*- coding: utf-8; -*-

# Copyright (C) 2015 - 2020 Lionel Ott
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

from __future__ import annotations

from abc import abstractmethod, ABCMeta

from typing import Any, List, Optional
import uuid
from xml.etree import ElementTree

from PySide6 import QtCore

from gremlin import error
from gremlin.event_handler import Event
from gremlin.profile_library import ActionTree
from gremlin.types import InputType

from gremlin.ui.profile import ActionNodeModel


class Value:

    """Represents an input value, keeping track of raw and "seen" value."""

    def __init__(self, raw):
        """Creates a new value and initializes it.

        :param raw the initial raw data
        """
        self._raw = raw
        self._current = raw

    @property
    def raw(self):
        """Returns the raw unmodified value.

        :return raw unmodified value
        """
        return self._raw

    @property
    def current(self):
        """Returns the current, potentially, modified value.

        :return current and potentially modified value
        """
        return self._current

    @current.setter
    def current(self, current):
        """Sets the current value which may differ from the raw one.

        :param current the new current value
        """
        self._current = current


class AbstractActionModel(QtCore.QObject):

    """Base class for all action related data calsses."""

    modelChanged = QtCore.Signal()

    def __init__(
            self,
            action_tree: ActionTree,
            behavior_type: InputType=InputType.JoystickButton,
            parent: Optional[QtCore.QObject]=None
    ):
        super().__init__(parent)

        self._id = uuid.uuid4()
        self._action_tree = action_tree
        self._behavior_type = behavior_type

    @property
    def id(self) -> uuid.UUID:
        """Returns the identifier of this action.

        Returns:
            Unique identifier of this action
        """
        return self._id

    @property
    def behavior_type(self) -> InputType:
        return self._behavior_type

    def set_behavior_type(self, new_behavior: InputType):
        old_behavior = self._behavior_type
        self._behavior_type = new_behavior
        if old_behavior != new_behavior:
            self._handle_behavior_change(old_behavior, new_behavior)

    def qml_path(self) -> str:
        """Returns the path to the QML file visualizing the action.

        Returns:
            String representation of the QML file path
        """
        raise error.MissingImplementationError(
            "AbstractActionModel.qml_path not implemented in subclass"
        )

    def from_xml(self, node: ElementTree.Element) -> None:
        """Populates the instance's values with the content of the XML node.

        Args:
            node: the XML node to parse for content
        """
        raise error.MissingImplementationError(
            "AbstractActionModel.from_xml not implemented in subclass"
        )

    def to_xml(self) -> ElementTree.Element:
        """Returns an XML node representing the instance's contents.

        Returns:
            XML node containing the instance's contents
        """
        raise error.MissingImplementationError(
            "AbstractActionModel.to_xml not implemented in subclass"
        )

    def is_valid(self) -> bool:
        """Returns whether or not the instance is in a valid state.

        Returns:
            True if the instance is in a valid state, False otherwise
        """
        raise error.MissingImplementationError(
            "AbstractActionModel.is_valid not implemented in subclass"
        )

    def remove_action(self, action: AbstractActionModel) -> None:
        """Removes the provided action from this action.

        Args:
            action: the action to remove
        """
        pass

    def add_action_after(
        self,
        anchor: AbstractActionModel,
        action: AbstractActionModel
    ) -> None:
        """Adds the provided action after the specified anchor.

        Args:
            anchor: action after which to insert the given action
            action: the action to remove
        """
        pass

    def insert_action(self, container: str, action: AbstractActionModel) -> None:
        """Inserts the action into a specific container.

        Args:
            container: label of the container into which to insert the
                provided action
            action: the action to insert
        """
        raise error.MissingImplementationError(
            "AbstractActionModel.insert_action not implemented in subclass"
        )

    def _handle_behavior_change(
        self,
        old_behavior: InputType,
        new_behavior: InputType
    ) -> None:
        """Handles changing of the behavior type of the action.

        This function will only be called when the two behaviors are different.

        Args:
            old_behavior: type describing the old behavior
            new_behavior: type describing the new behavior
        """
        pass

    def _create_node_list(self, action_ids):
        nodes = []
        for node in self._action_tree.root.nodes_matching(
            lambda x: x.value.id in action_ids
        ):
            node.value.setParent(self)
            nodes.append(ActionNodeModel(
                node,
                self.behavior_type,
                self._action_tree,
                parent=self
            ))
        return nodes

    def _remove_from_list(self, storage: List[Any], value: Any) -> None:
        """Removes the provided value from the list storage.

        Args:
            storage: list object from which to remove the value
            value: value to remove
        """
        if value in storage:
            storage.remove(value)

    def _insert_into_list(
        self,
        storage: List[Any],
        anchor: Any,
        value: Any,
        append: bool=True
    ) -> None:
        """Inserts the given value into the storage.

        Args:
            storage: list object into which to insert the value
            anchor: value around which to insert the new value
            value: new value to insert into the list
            append: append if True, prepend if False
        """
        if anchor in storage:
            index = storage.index(anchor)
            index = index + 1 if append else index
            storage.insert(index, value)


class AbstractFunctor(metaclass=ABCMeta):

    """Abstract base class defining the interface for functor like classes.

    TODO: Rework this thing

    These classes are used in the internal code execution system.
    """

    def __init__(self, instance: AbstractActionModel):
        """Creates a new instance, extracting needed information.

        :param instance the object which contains the information needed to
            execute it later on
        """
        self.data = instance

    @abstractmethod
    def process_event(self, event: Event, value: Value) -> None:
        """Processes the functor using the provided event and value data.

        :param event the raw event that caused the functor to be executed
        :param value the possibly modified value
        """
        pass
