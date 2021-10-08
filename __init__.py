# ##### BEGIN GPL LICENSE BLOCK #####
#
# <Keep track of your Blender-Behavior>
#  Copyright (C) <2020>  <Blender Defender>
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 3
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####


import os
from os import path as p

import shutil

from . import (
    prefs,
    panels,
    operators,
)

from .functions import (
    handler_functions
)

from .functions.main_functions import (
    update_json,
)

from .functions.register_functions import (
    date_unregister
)

bl_info = {
    "name": "Super Easy Analytics (SEA)",
    "author": "Blender Defender",
    "version": (1, 1, 0),
    "blender": (2, 83, 0),
    "location": "Sidebar (N) > View > Super Easy Analytics",
    "description": "Analyze your Blender behavior!",
    "warning": "Checkout Gumroad for other Addons and more...",
    "wiki_url": "https://github.com/BlenderDefender/SuperEasyAnalytics/wiki",
    "tracker_url": "https://github.com/BlenderDefender/SuperEasyAnalytics/issues",
    "endpoint_url": "https://raw.githubusercontent.com/BlenderDefender/BlenderDefender/updater_endpoints/SUPEREASYANALYTICS.json",
    "category": "Analytics"
}


modules = (
    operators,
    panels,
    handler_functions
)

# Path to the Super Easy Analytics Data directory.
PATH = p.join(p.expanduser(
    "~"), "Blender Addons Data", "blender-analytics", "data.json")


def register() -> None:
    # Create the Super Easy Analytics Data Directory, if it doesn't exist already.
    if not p.isdir(p.dirname(PATH)):
        os.makedirs(p.dirname(PATH))

    # Update the JSON Data file, if it doesn't work with the latest version of Super Easy Analytics.
    if p.exists(PATH):
        update_json(PATH)
    else:  # Copy data.json to the Super Easy Analytics Data directory, if it doesn't already exist.
        shutil.copyfile(p.join(p.dirname(__file__),
                               "functions",
                               "data.json"),
                        PATH)

    prefs.register(bl_info)

    for mod in modules:
        mod.register()


def unregister() -> None:
    for mod in reversed(modules):
        mod.unregister()

    prefs.unregister()

    date_unregister(PATH)
