# -*- coding: utf-8; -*-

# Copyright (C) 2015 - 2022 Lionel Ott
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

"""
Main UI of JoystickGremlin.
"""

import argparse
import ctypes
import logging
import os
import sys
import time
import traceback


# Import QtMultimedia so pyinstaller doesn't miss it
from PySide6 import QtCore, QtGui, QtQml, QtQuick, QtWidgets

import resources

import dill

# Figure out the location of the code / executable and change the working
# directory accordingly
install_path = os.path.normcase(os.path.dirname(os.path.abspath(sys.argv[0])))
os.chdir(install_path)

# Setting some global QT configurations
os.environ["QT_QUICK_CONTROLS_STYLE"] = "Universal"
# os.environ["QT_QUICK_CONTROLS_MATERIAL_VARIANT"] = "Normal"
os.environ["QT_QUICK_CONTROLS_UNIVERSAL_THEME"] = "Light"
#os.environ["QT_QUICK_CONTROLS_HOVER_ENABLED"] = "true"
# os.environ["QML_IMPORT_TRACE"] = "1"
# os.environ["QSG_RHI"] = "1"

import gremlin.error
import gremlin.plugin_manager
import gremlin.types
import gremlin.signal
import gremlin.util

import gremlin.ui.backend
import gremlin.ui.config
import gremlin.ui.device
import gremlin.ui.profile
import gremlin.ui.util


def configure_logger(config):
    """Creates a new logger instance.

    :param config configuration information for the new logger
    """
    logger = logging.getLogger(config["name"])
    logger.setLevel(config["level"])
    handler = logging.FileHandler(config["logfile"])
    handler.setLevel(config["level"])
    formatter = logging.Formatter(config["format"], "%Y-%m-%d %H:%M:%S")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    logger.debug("-" * 80)
    logger.debug(time.strftime("%Y-%m-%d %H:%M"))
    logger.debug("Starting Joystick Gremlin R14")
    logger.debug("-" * 80)


def exception_hook(exception_type, value, trace):
    """Logs any uncaught exceptions.

    :param exception_type type of exception being caught
    :param value content of the exception
    :param trace the stack trace which produced the exception
    """
    msg = "Uncaught exception:\n"
    msg += " ".join(traceback.format_exception(exception_type, value, trace))
    logging.getLogger("system").error(msg)
    gremlin.util.display_error(msg)


def shutdown_cleanup():
    """Handles cleanup before terminating Gremlin."""
    # Terminate potentially running EventListener loop
    event_listener = gremlin.event_handler.EventListener()
    event_listener.terminate()

    # Terminate profile runner
    backend = gremlin.ui.backend.Backend()
    backend.runner.stop()

    # Relinquish control over all VJoy devices used
    gremlin.joystick_handling.VJoyProxy.reset()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--profile",
        help="Path to the profile to load on startup",
    )
    parser.add_argument(
        "--enable",
        help="Enable Joystick Gremlin upon launch",
        action="store_true"
    )
    parser.add_argument(
        "--start-minimized",
        help="Start Joystick Gremlin minimized",
        action="store_true"
    )
    args = parser.parse_args()

    # Path manging to ensure Gremlin starts independent of the CWD
    sys.path.insert(0, gremlin.util.userprofile_path())
    gremlin.util.setup_userprofile()

    # Configure logging for system and user events
    configure_logger({
        "name": "system",
        "level": logging.DEBUG,
        "logfile": os.path.join(gremlin.util.userprofile_path(), "system.log"),
        "format": "%(asctime)s %(levelname)10s %(message)s"
    })
    configure_logger({
        "name": "user",
        "level": logging.DEBUG,
        "logfile": os.path.join(gremlin.util.userprofile_path(), "user.log"),
        "format": "%(asctime)s %(message)s"
    })

    syslog = logging.getLogger("system")

    # Show unhandled exceptions to the user when running a compiled version
    # of Joystick Gremlin
    executable_name = os.path.split(sys.executable)[-1]
    if executable_name == "joystick_gremlin.exe":
        sys.excepthook = exception_hook

    # Initialize QT components
    #QtWebEngine.QtWebEngine.initialize()

    # Prevent blurry fonts that Qt seems to like
    # QtQuick.QQuickWindow.setTextRenderType(
    #     QtQuick.QQuickWindow.NativeTextRendering
    # )
    # Use software rendering to prevent flickering on variable refresh rate
    # displays
    # QtQuick.QQuickWindow.setSceneGraphBackend("software")
    QtQuick.QQuickWindow.setGraphicsApi(QtQuick.QSGRendererInterface.OpenGL)

    # Create user interface
    app_id = u"joystick.gremlin"
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon("gfx/icon.png"))
    app.setApplicationDisplayName("Joystick Gremlin")

    # Configure QSettings to keep QT happy
    app.setOrganizationName("H2IK")
    app.setOrganizationDomain("http://whitemagic.github.io/JoystickGremlin/")
    app.setApplicationName("Joystick Gremlin")

    # Ensure joystick devices are correctly setup
    dill.DILL.init()
    gremlin.joystick_handling.joystick_devices_initialization()

    # Create application and UI engine
    engine = QtQml.QQmlApplicationEngine(parent=app)
    QtCore.QDir.addSearchPath(
        "core_plugins",
        gremlin.util.resource_path("action_plugins/")
    )


    # +-------------------------------------------------------------------------
    # | Register data types for use in QML
    # +-------------------------------------------------------------------------

    # Create backend instance and register it in the engine
    backend = gremlin.ui.backend.Backend()
    engine.rootContext().setContextProperty("backend", backend)
    engine.rootContext().setContextProperty("signal", gremlin.signal.signal)

    # Load plugin code and UI elements
    syslog.info("Initializing plugins")
    gremlin.plugin_manager.ActionPlugins()

    # Load icon fonts
    if QtGui.QFontDatabase.addApplicationFont(":/BootstrapIcons") < 0:
        syslog.error("Failed to load BootstrapIcons")

    # Initialize main UI
    engine.load(QtCore.QUrl.fromLocalFile("qml/Main.qml"))
    if not engine.rootObjects():
        sys.exit(-1)

    # Check if vJoy is properly setup and if not display an error
    # and terminate Gremlin
    # try:
    #     syslog.info("Checking vJoy installation")
    #     vjoy_working = len([
    #         dev for dev in gremlin.joystick_handling.joystick_devices()
    #         if dev.is_virtual
    #     ]) != 0
    #
    #     if not vjoy_working:
    #         logging.getLogger("system").error(
    #             "vJoy is not present or incorrectly setup."
    #         )
    #         raise gremlin.error.GremlinError(
    #             "vJoy is not present or incorrectly setup."
    #         )
    #
    # except (gremlin.error.GremlinError, dill.DILLError) as e:
    #     error_display = QtWidgets.QMessageBox(
    #         QtWidgets.QMessageBox.Critical,
    #         "Error",
    #         e.value,
    #         QtWidgets.QMessageBox.Ok
    #     )
    #     error_display.show()
    #     app.exec_()
    #
    #     gremlin.joystick_handling.VJoyProxy.reset()
    #     event_listener = gremlin.event_handler.EventListener()
    #     event_listener.terminate()
    #     sys.exit(0)

    # Handle user provided command line arguments
    if args.profile is not None and os.path.isfile(args.profile):
        backend.loadProfile(args.profile)
    # if args.enable:
    #     ui.ui.actionActivate.setChecked(True)
    #     ui.activate(True)
    # if args.start_minimized:
    #     ui.setHidden(True)

    # Run UI
    syslog.info("Gremlin UI launching")
    app.aboutToQuit.connect(shutdown_cleanup)
    app.exec()
    syslog.info("Gremlin UI terminated")

    syslog.info("Terminating Gremlin")
    sys.exit(0)
