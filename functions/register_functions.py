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
from bpy.props import (
    BoolProperty,
    FloatProperty,
    IntProperty
)

from os import path as p

import time

from .json_functions import (
    decode_json,
    encode_json
)

scene = bpy.types.Scene


def register_props():
    scene.default_cube_deleted = BoolProperty(
        name="Default cube deleted",
        default=False
    )
    scene.project_time = FloatProperty(
        name="Time spent on this file",
        default=0.0
    )
    scene.project_price = FloatProperty(
        name="How much do you get paid for this project?",
        default=0.0
    )
    scene.save_timestamp = IntProperty(
        name="Save timestamp"
    )
    scene.render_time = FloatProperty(
        name="Render time",
        default=0.0
    )
    scene.render_timestamp = FloatProperty(
        name="Render timestamp"
    )


# Save the date and time on Blender Startup.
def date_register(path):
    j = decode_json(path)
    date = [time.localtime()[2], time.localtime()[1], time.localtime()[0]]

    if j["date"] != date:
        j_date = time.strftime(
            "%Y-%m-%d", time.strptime(str(j["date"]), "[%d, %m, %Y]"))

        j["dates_hours_alignment"][j_date] = round(j["time_today"] / 60)
        j["date"] = date
        j["time_yesterday"] = round(j["time_today"] / 60)
        j["time_today"] = 0.00

    j["start_time"] = int(time.time())
    encode_json(j, path)


# Save the difference between the start date/time and the end date/time as Blender usage time.
# Save the current date/time as new start date/time.
def date_unregister(path):
    j = decode_json(path)

    current_time = int(time.time())

    total_seconds = current_time - j["start_time"]
    if total_seconds > 30:
        total_seconds = 0

    j["time_today"] += total_seconds
    bpy.project_time += total_seconds
    j["start_time"] = current_time

    encode_json(j, path)
