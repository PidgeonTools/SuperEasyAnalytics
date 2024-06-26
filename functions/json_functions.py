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

import json


def decode_json(path: str) -> dict:
    """Decode a JSON file.

    Args:
        path (str): The path of the JSON file.

    Returns:
        dict: The JSON data.
    """

    with open(path) as f:
        j = json.load(f)
    return j


def encode_json(j: dict, path: str) -> dict:
    """Encode a JSON file.

    Args:
        j (dict): The JSON data.
        path (str): The path to the JSON file.

    Returns:
        dict: The JSON data.
    """

    with open(path, "w") as f:
        json.dump(j, f, indent=4)
    return j
