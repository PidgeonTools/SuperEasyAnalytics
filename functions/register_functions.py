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


def register_props() -> None:
    """Register custom scene properties."""

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


def date_register(path: str) -> None:
    """Save the date and time on Blender Startup.

    Args:
        path (str): The path of the SEA data file.
    """

    # Get the SEA data.
    j = decode_json(path)

    # Get the current date.
    date = [time.localtime()[2], time.localtime()[1], time.localtime()[0]]

    if j["date"] != date:
        # Set the label for the dates_hours_alignment.
        label = time.strftime(
            "%Y-%m-%d", time.strptime(str(j["date"]), "[%d, %m, %Y]"))

        # Update the SEA data.
        j["dates_hours_alignment"][label] = round(j["time_today"] / 60)
        j["date"] = date
        j["time_yesterday"] = round(j["time_today"] / 60)
        j["time_today"] = 0.00

    # Set the start time.
    j["start_time"] = int(time.time())

    # Save the SEA data.
    encode_json(j, path)


def update_time_of_use(path: str) -> None:
    """Save the difference between the start date/time and the end date/time as Blender usage time.
    Save the current date/time as new start date/time.

    Args:
        path (str): The path of the SEA data file.
    """

    THRESHHOLD = 30

    # Get the SEA data.
    j = decode_json(path)

    # Get the current time
    current_time = int(time.time())

    # Calculate the total seconds since the last event.
    # Ignore the time, if nothing happened for longer than a certain threshhold.
    total_seconds = current_time - j["start_time"]
    if total_seconds > THRESHHOLD:
        total_seconds = 0

    # Add the calculated time to the data and update the start time.
    j["time_today"] += total_seconds
    bpy.project_time += total_seconds
    j["start_time"] = current_time

    # Save the SEA data.
    encode_json(j, path)
