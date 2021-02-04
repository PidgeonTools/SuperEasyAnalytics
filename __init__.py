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
import shutil

import json

import queue
from mathutils import *

import requests

from. import operators, prefs, panels

from .functions.mainFunctions import (
    check_for_cube,
    date_register,
    date_unregister,
    update_json,
)
from .functions.jsonFunctions import decode_json, encode_json

bl_info = {
    "name": "Blender Analytics",
    "author": "Blender Defender",
    "version": (1, 0, 1),
    "blender": (2, 83, 0),
    "location": "Sidebar (N) > View > Blender Analytics",
    "description": "Analyze your Blender behavior!",
    "warning": "Checkout Gumroad for other Addons and more...",
    "wiki_url": "https://gumroad.com/blenderdefender",
    "tracker_url": "https://github.com/BlenderDefender/Blender-Analytics/issues",
    "category": "Analytics"
}


def register():
    prefs.register(bl_info)
    operators.register()

    addon_prefs = bpy.context.preferences.addons[__package__].preferences

    global activate
    activate = True

    path = os.path.join(os.path.expanduser("~"), "Blender Addons Data", "blender-analytics")
    if not os.path.isdir(path):
        os.makedirs(path)

    if os.path.exists(os.path.join(path, "data.json")):
        try:
            j = decode_json(os.path.join(path, "data.json"))
            print(j["check_update"])

        except:
            update_json(os.path.join(path, "data.json"))
    else:
        shutil.copyfile(os.path.join(os.path.dirname(__file__),
                                     "functions",
                                     "data.json"),
                        os.path.join(path,
                                     "data.json"))

    db_path = os.path.join(path, "Blender Analytics e6017460ea3479e67886f3430845.db")
    if os.path.exists(db_path):
        if addon_prefs.fast_startup:
            data = decode_json(db_path)
            if not data["success"]:
                activate = False
        else:
            try:
                with open(os.path.join(path, "Blender Analytics c704d36c50269763b8bce4479f.db"), "r") as f:
                    key = f.read()

                permalink = "BlenderAnalytics"
                data = json.loads(requests.post("https://api.gumroad.com/v2/licenses/verify",
                                                data={"product_permalink": permalink,
                                                      "license_key": key,
                                                      "increment_uses_count": "false"}).text)
                encode_json(data, db_path)
                if not data["success"]:
                    activate = False
            except:
                data = decode_json(db_path)
                if not data["success"]:
                    activate = False

    else:
        try:
            with open(os.path.join(path, "Blender Analytics c704d36c50269763b8bce4479f.db"), "r") as f:
                key = f.read()

            permalink = "BlenderAnalytics"
            data = json.loads(requests.post("https://api.gumroad.com/v2/licenses/verify",
                                            data={"product_permalink": permalink,
                                                  "license_key": key,
                                                  "increment_uses_count": "false"}).text)
            encode_json(data, db_path)
            if not data["success"]:
                activate = False

        except:
            activate = False

    if activate:
        panels.register()

        global t
        t = queue.threading.Timer(40, lambda: check_for_cube(bpy.data.meshes['Cube'].users,
                                                             os.path.join(path, "data.json")))
        t.start()

        date_register(os.path.join(path, "data.json"))


def unregister():
    prefs.unregister()
    operators.unregister()

    if activate:
        panels.unregister()

        t.cancel()

        path = os.path.join(os.path.expanduser("~"),
                            "Blender Addons Data",
                            "blender-analytics",
                            "data.json")
        date_unregister(path)
