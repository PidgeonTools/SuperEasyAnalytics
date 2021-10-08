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

import time

from bpy.types import (
    Context,
    Scene
)

from .json_functions import (
    decode_json,
    encode_json
)


from .register_functions import (
    register_props,
    date_register
)

PATH = p.join(p.expanduser("~"), "Blender Addons Data",
              "blender-analytics", "data.json")


# Count the number of undos
@persistent  # Keep the function registered across multiple files.
def count_undo(*args):
    # Get the SEA data.
    data = decode_json(PATH)

    # Add undo count to data.json, if it doesn't exist.
    if not "undo_count" in data.keys():
        data["undo_count"] = 0

    # Increment the undo count by one.
    data["undo_count"] += 1

    # Encode the SEA data.
    encode_json(data, PATH)


@persistent  # Keep the function registered across multiple files.
def startup_setup(*args):
    context: Context = bpy.context
    scene: Scene = context.scene

    # Save the date/time at startup.
    date_register(PATH)

    # Register all custom properties in the file.
    if not hasattr(scene, "save_timestamp"):
        register_props()

    # Add the project_time attribute to bpy, because bpy.context is read-only in draw()
    bpy.project_time = context.scene.project_time
    print(bpy.ops.supereasyanalytics.modal())  # Debugging only


@persistent  # Keep the function registered across multiple files.
def save_project_time(*args):
    context: Context = bpy.context
    context.scene.project_time = bpy.project_time


@persistent  # Keep the function registered across multiple files.
def set_save_timestamp(*args):
    context: Context = bpy.context
    context.scene.save_timestamp = int(time.time())


@persistent  # Keep the function registered across multiple files.
def set_render_timestamp(*args):
    context: Context = bpy.context
    context.scene.render_timestamp = time.time()


# Save the render time to bpy.context after rendering.
@persistent  # Keep the function registered across multiple files.
def set_render_time(*args):
    context: Context = bpy.context
    render_timestamp = context.scene.render_timestamp
    context.scene.render_time += time.time() - render_timestamp


def register():
    bpy.app.handlers.load_post.append(startup_setup)
    bpy.app.handlers.undo_post.append(count_undo)
    bpy.app.handlers.save_pre.append(save_project_time)
    bpy.app.handlers.save_pre.append(set_save_timestamp)
    bpy.app.handlers.render_init.append(set_render_timestamp)
    bpy.app.handlers.render_complete.append(set_render_time)
    bpy.app.handlers.render_cancel.append(set_render_time)


def unregister():
    bpy.app.handlers.load_post.remove(startup_setup)
    bpy.app.handlers.undo_post.remove(count_undo)
    bpy.app.handlers.save_pre.remove(save_project_time)
    bpy.app.handlers.save_pre.remove(set_save_timestamp)
    bpy.app.handlers.render_init.remove(set_render_timestamp)
    bpy.app.handlers.render_complete.remove(set_render_time)
    bpy.app.handlers.render_cancel.remove(set_render_time)
