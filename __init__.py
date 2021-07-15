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

from .functions.mainFunctions import (
    check_for_cube,
    date_register,
    date_unregister,
    update_json,
)
import bpy

import os
from os import path as p

import shutil

import queue

from . import prefs, panels
from .functions.jsonFunctions import decode_json


bl_info = {
    "name": "Blender Analytics",
    "author": "Blender Defender",
    "version": (1, 1, 0),
    "blender": (2, 83, 0),
    "location": "Sidebar (N) > View > Blender Analytics",
    "description": "Analyze your Blender behavior!",
    "warning": "Checkout Gumroad for other Addons and more...",
    "wiki_url": "https://gumroad.com/blenderdefender",
    "tracker_url": "https://github.com/BlenderDefender/Blender-Analytics/issues",
    "endpoint_url": "https://raw.githubusercontent.com/BlenderDefender/BlenderDefender/updater_endpoints/BLENDERANALYTICS.json",
    "category": "Analytics"
}


def register():
    prefs.register(bl_info)
    panels.register()

    # Path to the Blender Analytics Data directory.
    path = p.join(p.expanduser(
        "~"), "Blender Addons Data", "blender-analytics")

    # Create the Blender Analytics Data Directory, if it doesn't exist already.
    if not p.isdir(path):
        os.makedirs(path)

    # Update the JSON Data file, if it doesn't work with the latest version of Blender Analytics.
    if p.exists(p.join(path, "data.json")):
        update_json(p.join(path, "data.json"))
    else:  # Copy data.json to the Blender Analytics Data directory, if it doesn't already exist.
        shutil.copyfile(p.join(p.dirname(__file__),
                               "functions",
                               "data.json"),
                        p.join(path,
                               "data.json"))

    # Start the default cube counter.
    global t
    t = queue.threading.Timer(40, lambda: check_for_cube(bpy.data.meshes['Cube'].users,
                                                         p.join(path, "data.json")))
    t.start()

    # Save the date/time at startup.
    date_register(p.join(path, "data.json"))


def unregister():
    prefs.unregister()
    panels.unregister()

    # Stop the default cube counter to avoid errors.
    t.cancel()

    # Write the usage time to data.json!
    path = p.join(p.expanduser("~"),
                  "Blender Addons Data",
                  "blender-analytics",
                  "data.json")
    date_unregister(path)
