// -*- coding: utf-8; -*-
//
// Copyright (C) 2015 - 2022 Lionel Ott
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.


import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import Gremlin.ActionPlugins

import "../../qml"


Item {
    id: _root

    property RangeComparator comparator

    implicitHeight: _content.height
    implicitWidth: _content.width

    RowLayout {
        id: _content

        Label {
            text: "This input is between"
        }

        FloatSpinBox {
            id: _lower

            minValue: -1.0
            maxValue: _upper.value
            stepSize: 0.05
            realValue: _root.comparator.lowerLimit

            onRealValueModified: function() {
                _root.comparator.lowerLimit = realValue
            }
        }

        Label {
            text: "and"
        }

        FloatSpinBox {
            id: _upper

            minValue: _lower.value
            maxValue: 1.0
            stepSize: 0.05
            realValue: _root.comparator.upperLimit

            onRealValueModified: function() {
                _root.comparator.upperLimit = realValue
            }
        }
    }
}