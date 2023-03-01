# QML Notes

This contains a collection of good to know things when working with QML and Python. Before anything else you should read this book in its entirety [Qt6 QML Book](https://www.qt.io/product/qt6/qml-book).

## Property Binding

One of the nice properties of QML is that it has property binding, i.e. it can be directly fed with values from any `QtObject` based instance if it exposes its values properly. This can be achieved through the following:

```python
from PySide6 import QtCore, QtQML

class DemoModel(QtCore.QObject):

    variableChanged = QtCore.Signal()

    def __init__(self, parent=None)
        super().__init__(parent)

        self._variable = "Test"

    def _get_variable(self) -> str:
        return self._variable

    def _set_variable(self, value: str) -> None:
        if value == self._variable:
            return

        self._variable = value
        self.variableChanged.emit()

    variable = QtCore.Property(
        str,
        fget=_get_variable,
        fset=_set_variable,
        notify=variableChanged
    )
```

The above skeleton exposes the `variable` member to QML and will notify the QML side when the value of `variable` is changed. However, if the QML content representing the value of `variable` changes this is not sent back to the Python side. Apparently this two way communication is not support by QML and given this was the case back in 2010 it does not seem likely to ever be added. In order to support such a two way synchronization the QML side needs to actively updated the Python side.

```qml
Item {
    property DemoModel model

    TextField {
        text: model.variable

        onTextChanged: {
            model.variable = text
        }
    }
}
```

The above QML snippet populates the textfield with the value of the `variable` from the above model class. Any changes to the value of `variable` via Python code will notify the QML side and update the visual representation accordingly. To send changes back to the Python model instance the `onTextChanged` signal needs to added. To prevent a binding loop the `_set_variable` method needs to ensure the provided value is different from the currently stored one, as otherwise a event loop would be possible.

## Property pass-through and aliasing

Complex widgets are often composed of multiple QML types which have properties that one wants to set on the widget rather than the subcomponent level. To achieve this the main part of the widget has to expose those properties via an alias property. The property being exposed does not have to be specifically set in the child component if it is a property that is exposed by that component by default.

```
Item {
	property alias text: _label.text
	
	RowLayout {
		Label {
			id: _label
		}
	}
}
```

## Python Function Return Values for QML

It is possible to call Python functions which return a value from QML as long as these are defined as `Slot` in a `QtCore` derived class. The `gremlin.ui.backend` class is a good example of a class making use of this.

```python
import random

from PySide6 import QtCore

class Backend(QtCore):

    def __init__(self, parent=None):
        super().__init__(parent)

    @QtCore.Slot(int, int, result=int)
    def randomInt(self, min_val: int, max_val: int) -> int:
        return random.randint(min_val, max_val)
```

This allows the method to be called from within any QML file which has access to the an instance of the `Backend` class.

## Model Classes with Custom Attribute Names

Accessing data from a Python model via custom names is the more convenient then having to deal with possibly changing indices. This is readily supported by QML by specifying additional model roles in the Python model being visualized via QML.

```python
from typing import Any, Dict
from PySide6 import QtCore, QtQML

class ColorModel(QtCore.QAbstractListModel):

    roles = {
        QtCore.Qt.UserRole + 1: QtCore.QByteArray("name".encode()),
        QtCore.Qt.UserRole + 2: QtCore.QByteArray("rgb".encode()),
    }

    def __init__(self, parent: None):
        super().__init__(parent)

        self._colors = []

    def rowCount(self, parent: QtCore.QModelIndex=...) -> int:
        return len(self._colors)

    def data(self, index: QtCore.QModelIndex, role: int=...) -> Any:
        if role not in ColorModel.roles:
            raise("Invalid role specified")

        role_name = SimpleModel.roles[role].data().decode()
        if role_name == "name":
            return self._colors[index.row].name
           elif role_name == "rgb":
            return self._colors[index.row].rgb

    def roleNames(self) -> Dict:
        return ColorModel.roles
```

The above example specifies a simple class which holds colors. To permit QML to access the properties, i.e. name and rgb code, of each color via name the `roles` dictionary is defined and exposed. Without this there is no way to access these properties via name.

## ListView

Frequently models will contain a list of identical items that need to be visualized. As these items might be taking up more space then the `ListView` component has in the UI it is capable of scrolling. To turn the `ListView` into a container that has a scroll bar and behaves properly, i.e. like a desktop application and not a phone app the following setup is recommended.

```qml
ListView {
    id: idListView
    anchors.fill: parent

    // Make it behave like a sensible scrolling container
    ScrollBar.vertical: ScrollBar {}
    flickableDirection: Flickable.VerticalFlick
    boundsBehavior: Flickable.StopAtBounds

    // Content to visualize
    model: model
    delegate: idDelegate
}

Component {
    id: idDelegate

    ...
}
```

## Simple List Models

At times it is useful to return a simple list of strings to be displayed by a QML view or repeater. Providing the model via property causes some issues as QML is not happy with the actual data types exposed by PySide6. As such to specify the correct type of `QVariantList` the type information has to be provided as a string.

```python
from PySide6 import QtCore

@QtCore.Property(type="QVariantList")
def listData():
    return ["List", "of", "Strings"]
```

This model can now be used by any QML element that can handle a list model.

## Drag & Drop

To implement drag & drop with QML three components are needed.

- The item to be dragged has to specify the correct `Drag.*` properties
- An area which acts as the drag handle has to be specified using, for example, a `MouseArea`
- An area onto which the dragged object can be dropped has to be specified using the `DropArea`

The behavior of the drag & drop system changes drastically based on the `Drag.dragType` value. Using the default value the `Drag.onDragStarted` event is not available (likely others not either). The setup that worked out for the desired behavior in Gremlin is the following:

**Item Drag values**

```qml
Drag.dragType: Drag.automatic
Drag.active: idDragArea.drag.active
Drag.supportedActions: Qt.MoveAction
Drag.proposedAction: Qt.MoveAction
Drag.mimeData: {
    "text/plain": model.id
}

Drag.onDragFinished: {
    idBaseItem.dragSuccess = dropAction == Qt.MoveAction;
}
Drag.onDragStarted: {
    idBaseItem.sourceY = idBaseItem.y
}
```

**Drag handle**

```qml
MouseArea {
    id: idDragArea

    drag.target: idBaseItem
    drag.axis: Drag.YAxis

    onReleased: {
        if(!idBaseItem.dragSuccess)
        {
            // Reset item position
        }
    }

    // Create an image of the object to visualize the dragging
    onPressed: idBaseItem.grabToImage(function(result) {
        idBaseItem.Drag.imageSource = result.url
    })
}
```

**Drop Area**

```qml
DropArea {
    id: idDropArea

    height: idBaseItem.height
    anchors.left: idBaseItem.left
    anchors.right: idBaseItem.right
    anchors.top: idBaseItem.verticalCenter

    // Visualization of the drop indicator
    Rectangle {
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.verticalCenter

        height: 5

        opacity: idDropArea.containsDrag ? 1.0 : 0.0
        color: "red"
    }

    onDropped: {
        // Signal that the drop was successful
        drop.accept();

        // Handle model change
        if(drop.text != model.id)
        {
            idListView.model.moveAfter(drop.text, model.id);
        }
    }
}
```

The above is not a generic setup that can be directly used as it relies on and makes assumptions about the model and intended behavior. However, the general flow should be applicable to other UI elements. The base item's `Drag.onDragFinished` sets a flag which is used by the `MouseArea.onReleased` event to reset the position of the item if needed. The `DropArea.onDropped` event handler ensures the `Drag.onDragFinished` is notified of success and then goes on to handle model changes that are in line with the intended drag & drop behavior.

### Action Drag & Drop

The most common items that will require drag & drop support are actions and action trees. In order to have a uniform appearance and reduce code duplication three QML widgets have been created which support the creation of a drop area. The drag component is not created inside an action but at a higher level and thus does not need to be considered for actions.

- `DropMarker` shows a rectangular area when a drag event of the correct type enters its area
- `DragDropArea` handles the logic of defining a `DropArea` and ensuring only valid drag events are reacted to
- `ActionDragDropArea` is a specialization of the `DragDropArea` widget for use specifically with action items

The `DragDropArea` and `ActionDragDropArea` widgets have the following properties that can be specified in order to customize the widgets.

- `target` the widget to which the drop area is being attached to and placed around
- `dropCallback` function to execute when a valid drop action occurs, the callback has one parameter `drop` which contains information about the item being dropped, as mime data
- `validationCallback` is called whenever a drag enters the `DropArea` to decide whether or not the drag event is compatible with the current area. This callback is already specified and configured for the `ActionDragDropArea` widget

In addition to these custom properties the usual properties of a `DropArea` are available as well. To adjust the placement of the widget specifying the `y` property may be required, especially if an item is changing position dynamically.

```
ActionDragDropArea {
    target: _placementIdentifier
    dropCallback: function(drop) {
    	// Action specific code to execute
    }
}
```



## Icon Colors

Icons on buttons and the like by default will be rendered black and white. This is caused by the tinting ability associated with colors. To display the icon's actual colors the `color` property of the `icon` has to be set to `transparent`.

```qml
// This results in the icon being shown using the colors defined in the image file
Button {
    icon.source: "path/to/icon.png"
    icon.color: "transparent"
}

// This results in the icon being shown in red
Button {
    icon.source: "path/to/icon.png"
    icon.color: "red"
}
```

## Python Object to QML Life Time

Returning a QML object instance from Python to QML code will in most cases fail to work as the Python object will be cleaned up, resulting in QML seeing a `null` object. The correct way to work around this is to use the `parent` parameter available to every `QtObject` based class. As such when creating an object in Python which is intended as a return type to QML UI code the `parent` parameter of the object should never be `None` but rather an instance of another QML object which will persist longer than the new object being created.

## Base Plugin UI Layout

To make new plugins render properly in the UI the following template should be followed. If this is not done there is a good chance that the plugin will not use all available space or be drawn across other elements.

```qml
import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQuick.Layouts 1.14

Item {
    height: _layout.height

    RowLayout {
        id: _layout

        anchors.left: parent.left
        anchors.right: parent.right

        Label {
            Layout.preferredWidth: 150
            text: "Description"
        }
        Label {
            Layout.fillWidth: true
            text: "Using the remaining space"
        }
    }
}
```

The above setup exploits the fact that when the plugin's UI code is dynamically created the height of the plugin is retrieved from this UI element while the width is dictated by the parent element in which this UI element is embedded. This UI element is resized during creation to with within the parent's width.

## Resource file generation

The `pyside6-rcc` programs converts the contents of a QRC file into a python module which can be loaded and used later on. When a venv is used the program resides within the scripts folder. Invoking the program takes the following form.

```bash
.\venv\Scripts\pyside6-rcc.exe .\resources.qrc -o .\resources.py
```



## Signal Inheritance

Dealing with signals in an inheritance hierarchy is somewhat annoying, as defining a property in a derived class using a signal defined in a parent doesn't work. As such, signals and properties have to be defined in the same class. To make matters worse the definition of the property binds the setter and getter function of the class in which the property is defined, making it impossible to redirect to a derived class' implementation. A solution around this is to have the actual setter/getter implementation be relegated to an implementation method which can be overriden in a derived class.

```python
from PySide6 import QtCore
from PySide6.QtCore import Signal, Property


class Base(QtCore.QObject):

    updated = Signal()

    def __init__(self):
        super().__init__()

        self._value = ""
    def _get_value(self) -> str:
        return self._get_value_impl()

    def _get_value_impl(self) -> str:
        return self._value

    def _set_value(self, new_value: str) -> None:
        self._set_value_impl(new_value)

    def _set_value_impl(self, new_value: str) -> None:
        if self._value != new_value:
            self._value = new_value
            self.updated.emit()

    value = Property(
        str,
        _get_value,
        _set_value,
        notify=updated
    )


class Derived(Base):

    def __init__(self):
        super().__init__()

    def _get_value_impl(self) -> str:
        return self.value.capitalize()
```

This scheme allows redefining the behvaiour by reimplementing the implementation method where desired.

## Component vs. Item

A `Component` is effectively a class, i.e. a template of what an instantiation will look like. As such a `Component` does not represent a specific object but can be used to create them. This can happen via the use in a delegate which will create an instance for each entry in the model. Another option is for dynamic object creation via the `createObject()` function of the `Component`.

An `Item` on the other hand is an explicitly existing object that is rendered and exists as defined. Its main purpose is the creation of complex user defined widgets that can be integrated to build up a custom UI.

A typical use of `Component` definitions is to define a reusable component inside a QML file, rather than having to create an entirely new QML file that would implement the desired component.

