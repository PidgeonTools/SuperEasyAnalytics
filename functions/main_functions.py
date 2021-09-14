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


import time

import os
from os import path as p

from .json_functions import (
    decode_json,
    encode_json
)


# Check, if the default cube has been deleted.
def check_for_cube(context, data, path):
    already_counted = context.scene.default_cube_deleted
    cube_deleted = False

    if "Cube" in data.meshes.keys():
        cube_deleted = data.meshes['Cube'].users == 0

    if cube_deleted and not already_counted:
        j = decode_json(path)

        j["default_cube"] += 1
        context.scene.default_cube_deleted = True

        encode_json(j, path)


# Get the usage time from yesterday.
def get_yesterday(path):
    return decode_json(path)["time_yesterday"]


# Get the usage time from today.
def get_today(path):
    return round(decode_json(path)["time_today"] / 60)


# Get the usage time from the last week
def get_last_week(path):
    data = decode_json(path)
    current_time = time.time()
    time_last_week = round(data["time_today"] / 60)

    DAY_IN_SECONDS = 60 * 60 * 24
    FORMAT = "%Y-%m-%d"

    for i in range(1, 8):
        day = time.strftime(FORMAT, time.localtime(
            current_time - i * DAY_IN_SECONDS))
        if day in data["dates_hours_alignment"].keys():
            time_last_week += data["dates_hours_alignment"][day]

    return time_last_week


# Get the count of deleted default cubes.
def get_default_cubes(path):
    return int(decode_json(path)["default_cube"])


def get_undos(path):
    data = decode_json(path)

    if "undo_count" in data.keys():
        return data["undo_count"]

    return 0


# Highlight an object with a vertex color.
def highlight_object(ob, set_color=False):
    if not ob.type == "MESH":
        return

    if "SEA_Highlight" in ob.data.vertex_colors:
        vc = ob.data.vertex_colors["SEA_Highlight"]
    else:
        vc = ob.data.vertex_colors.new(
            name="SEA_Highlight", do_init=False)
    vc.active = True

    if set_color:
        color = (0, 1, 0.0, 0)
    else:
        color = (1, 1, 1, 1)

    for data in vc.data:
        for c in data.color:
            print(c)
        data.color = color


# Update the data to version 1.0.1!
def update_json101(path):
    j = decode_json(path)

    j["check_update"] = 101

    for i in j["dates_hours_alignment"]:
        j["dates_hours_alignment"][i] = round(
            j["dates_hours_alignment"][i] * 60, 2)

    j["time_yesterday"] = round(j["time_yesterday"] * 60, 2)
    j["time_today"] = round(j["time_today"] * 60, 2)

    encode_json(j, path)


# Update the data to version 1.1.0!
def update_json_and_data110(path):
    j = decode_json(path)

    j["check_update"] = 110

    encode_json(j, path)

    db_filenames = ["Blender Analytics c704d36c50269763b8bce4479f.db",
                    "Blender Analytics e6017460ea3479e67886f3430845.db"]

    for file in db_filenames:
        file = p.join(p.dirname(path), file)
        if p.exists(file):
            os.remove(file)


def update_json_and_data120(path):
    FORMAT = "[%d, %m, %Y]"

    j = decode_json(path)

    elements = list(j["dates_hours_alignment"].keys())

    for i in elements:
        try:
            new_label = time.strftime("%Y-%m-%d", time.strptime(i, FORMAT))
        except Exception:
            continue
        j["dates_hours_alignment"][new_label] = j["dates_hours_alignment"].pop(
            i)

    j["check_update"] = 120

    encode_json(j, path)


# Checks the version of the JSON Data file and updates, if necessary.
def update_json(path):
    j = decode_json(path)

    if not "check_update" in j.keys():
        update_json101(path)

    if j["check_update"] == 101:
        update_json_and_data110(path)

    if j["check_update"] == 110:
        update_json_and_data120(path)
