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
import time

from os import path as p

from .jsonFunctions import (
    decode_json,
    encode_json
)


def check_for_cube(data):
    if data is 0:
        print("Default Cube deleted!")
        path = p.join(p.dirname(__file__), "data.json")
        j = decode_json(path)
        j["default_cube"] += 1
        encode_json(j, path)


def date_register():
    path = p.join(p.dirname(__file__), "data.json")
    j = decode_json(path)
    date = [time.localtime()[2], time.localtime()[1], time.localtime()[0]]
    current_time = [time.localtime()[3], time.localtime()[4], time.localtime()[5]]

    if j["date"] != date:
        j_date = str(j["date"])
        j["dates_hours_alignment"][j_date] = j["time_today"]
        j["date"] = date
        j["time_yesterday"] = j["time_today"]
        j["time_today"] = 0.00
    
    j["start_time"] = current_time
    encode_json(j, path)


def date_unregister():
    path = p.join(p.dirname(__file__), "data.json")
    j = decode_json(path)

    current_time = [time.localtime()[3], time.localtime()[4], time.localtime()[5]]

    hours = current_time[0] - j["start_time"][0]
    minutes = current_time[1] - j["start_time"][1]
    seconds = current_time[2] - j["start_time"][2]

    total_hours = hours + (minutes / 60) + (seconds / 3600)
    j["time_today"] += round(total_hours, 2)
    j["start_time"] = current_time

    encode_json(j, path)


def get_yesterday():
    path = p.join(p.dirname(__file__), "data.json")
    return decode_json(path)["time_yesterday"]


def get_today():
    path = p.join(p.dirname(__file__), "data.json")
    return decode_json(path)["time_today"]


def get_default_cubes():
    path = p.join(p.dirname(__file__), "data.json")
    return int(decode_json(path)["default_cube"])