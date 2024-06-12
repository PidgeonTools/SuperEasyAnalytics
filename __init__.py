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

import bpy

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
    upgrade_data_file,
    create_data_file
)

from .functions.register_functions import (
    update_time_of_use
)

bl_info = {
    "name": "Super Easy Analytics (SEA)",
    "author": "Blender Defender",
    "version": (1, 2, 1),
    "blender": (2, 83, 0),
    "location": "Sidebar (N) > View > Super Easy Analytics",
    "description": "Analyze your Blender behavior!",
    "warning": "Checkout Gumroad for other Addons and more...",
    "doc_url": "https://github.com/PidgeonTools/SuperEasyAnalytics/wiki",
    "tracker_url": "https://github.com/PidgeonTools/SuperEasyAnalytics/issues",
    "endpoint_url": "https://raw.githubusercontent.com/PidgeonTools/SAM-Endpoints/main/SuperEasyAnalytics.json",
    "category": "Analytics"
}


modules = (
    operators,
    panels,
    handler_functions
)

SEA_DATA_FOLDER = p.join(p.expanduser(
    "~"), "Blender Addons Data", "blender-analytics")
SEA_DATA_FILE = p.join(SEA_DATA_FOLDER, "data.json")


def register() -> None:
    if not p.isdir(SEA_DATA_FOLDER):
        os.makedirs(SEA_DATA_FOLDER)

    if p.exists(SEA_DATA_FILE):
        upgrade_data_file(SEA_DATA_FILE)
    else:
        create_data_file(SEA_DATA_FILE)

    if bpy.app.version < (4, 2):
        prefs.register_legacy(bl_info)
    else:
        prefs.register()

    for mod in modules:
        mod.register()


def unregister() -> None:
    for mod in reversed(modules):
        mod.unregister()

    prefs.unregister()

    update_time_of_use(SEA_DATA_FILE)
