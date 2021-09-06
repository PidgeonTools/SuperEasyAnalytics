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
from bpy.app.handlers import persistent

from os import path as p

from .json_functions import (
    decode_json,
    encode_json
)

from .main_functions import (
    date_register
)


# Count the number of undos
@persistent
def count_undo(*args):
    path = p.join(p.expanduser(
        "~"), "Blender Addons Data", "blender-analytics", "data.json")
    data = decode_json(path)

    if not "undo_count" in data.keys():
        data["undo_count"] = 0

    data["undo_count"] += 1

    encode_json(data, path)


@persistent
def startup_setup(*args):
    path = p.join(p.expanduser(
        "~"), "Blender Addons Data", "blender-analytics", "data.json")

    bpy.context.preferences.addons[__package__.split(
        ".")[0]].preferences.display_reminder = True

    # threading.Timer(5, lambda: test()).start()

    # Start the default cube counter.
    # global t
    # t = threading.Timer(40, lambda: check_for_cube(bpy.data.meshes['Cube'].users,
    #                                                p.join(path, "data.json")))
    # t.start()

    # Save the date/time at startup.
    date_register(path)

    print(bpy.ops.supereasyanalytics.modal())


def register():
    bpy.app.handlers.load_post.append(startup_setup)
    bpy.app.handlers.undo_post.append(count_undo)


def unregister():
    bpy.app.handlers.load_post.remove(startup_setup)
    bpy.app.handlers.undo_post.remove(count_undo)
