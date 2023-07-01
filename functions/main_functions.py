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


from posixpath import split
import bpy
from bpy.types import (
    Context,
    Object
)

import os
from os import path as p

import time

from .json_functions import (
    decode_json,
    encode_json
)


def check_for_cube(context: Context, data: bpy.data, path: str) -> bool:
    """Check, if the default cube has been deleted.

    Args:
        context (Context): The current Blender Context.
        data (bpy.data): The blend file data.
        path (str): The path of the SEA data file.

    Returns:
        bool: Whether the default cube has been deleted.
    """

    already_counted = context.scene.default_cube_deleted
    cube_deleted = False

    if "Cube" in data.meshes.keys():  # Check, that the default cube mesh exists.
        # The default cube was deleted, when it has 0 users.
        cube_deleted = data.meshes['Cube'].users == 0

    if cube_deleted and not already_counted:
        # Get the SEA data.
        j = decode_json(path)

        # Increment the default cube counter.
        j["default_cube"] += 1
        context.scene.default_cube_deleted = True

        # Encode the SEA data.
        encode_json(j, path)

        return cube_deleted

    return False


def get_yesterday(path: str) -> int:
    """Get the usage time from yesterday.

    Args:
        path (str): The path of the SEA data file.

    Returns:
        int: The usage time from yesterday.
    """

    return decode_json(path)["time_yesterday"]


def get_today(path: str) -> float:
    """Get the usage time from today.

    Args:
        path (str): The path of the SEA data file.

    Returns:
        float: The usage time from today.
    """

    return round(decode_json(path)["time_today"] / 60)


def get_last_week(path: str) -> float:
    """Get the usage time from the last week.

    Args:
        path (str): The path of the SEA data file.

    Returns:
        float: The usage time of the last week.
    """

    DAY_IN_SECONDS = 60 * 60 * 24
    FORMAT = "%Y-%m-%d"

    data = decode_json(path)  # Get the SEA data.
    current_time = time.time()  # Get the current time.

    # Initialise time_last_week to today's usage time.
    time_last_week = round(data["time_today"] / 60)

    for i in range(1, 8):  # yesterday to seven days ago
        # Generate a string of the day i, using the format of the SEA data file.
        day = time.strftime(FORMAT, time.localtime(
            current_time - i * DAY_IN_SECONDS))

        # Add the day i to the last weeks time, if it exists in the list.
        if day in data["dates_hours_alignment"].keys():
            time_last_week += data["dates_hours_alignment"][day]

    return time_last_week


def get_default_cubes(path: str) -> int:
    """Get the count of deleted default cubes.

    Args:
        path (str): The path of the SEA data file.

    Returns:
        int: The amount of deleted default cubes.
    """

    return int(decode_json(path)["default_cube"])


def get_undos(path: str) -> int:
    """Get the count of undos.

    Args:
        path (str): The path of the SEA data file.

    Returns:
        int: The amount of total undos.
    """

    data = decode_json(path)

    return data.get("undo_count", 0)


def get_render_devices(path: str) -> tuple:
    """Get, which render device was used how often.

    Args:
        path (str): The path of the SEA data file.

    Returns:
        tuple: The data, which render device was used how often.
    """

    data = decode_json(path)["rendering_devices"]

    most_used = max(data, key=data.get)

    return (most_used, data[most_used]), tuple(data.items())


def get_file_data() -> list:
    """Get the Blender File Data as list.

    Returns:
        list: The Blender file data list.
    """

    data = []

    # List of attributes to exclude from bpy.data
    blacklist = ["__doc__", "__module__", "__slots__", "batch_remove", "bl_rna", "is_dirty", "is_saved",
                 "rna_type", "use_autopack", "user_map", "version", "filepath", "orphans_purge", "temp_data"]

    # Go over all attributes of bpy.data
    for i in dir(bpy.data):
        if i in blacklist:
            continue

        # Get the attribute data.
        attribute = getattr(bpy.data, i)

        # Prevent errors when trying to convert to a list.
        if attribute == None:
            continue

        # Add the name and count to the data list, if the attribute contains data.
        if len(list(attribute)) > 0:
            pretty_name = " ".join([w.capitalize() for w in i.split("_")])
            data.append((pretty_name, len(list(attribute))))

    return data


def highlight_object(ob: Object, set_highlight_color=False) -> None:
    """Highlight an object using a vertex color.

    Args:
        ob (Object): The object to highlight.
        set_highlight_color (bool, optional): Whether to set or to unset the highlight color. Defaults to False.
    """

    # Abort, if the given object isn't a mesh.
    if ob.type != "MESH":
        return

    # Get the SEA Highlight Vertex Color or create it, if it doesn't exist.
    if "_SEA_Highlight" in ob.data.vertex_colors:
        vertex_color = ob.data.vertex_colors["_SEA_Highlight"]
    else:
        vertex_color = ob.data.vertex_colors.new(
            name="_SEA_Highlight", do_init=False)

    # Set the SEA Vertex Color active.
    vertex_color.active = True

    # Set the color, that the object should have.
    color = (1, 1, 1, 1)  # Transparent white
    if set_highlight_color:
        color = (0, 1, 0, 0)  # Green

    # Check, if the vertex color needs to be changed.
    set_color = tuple(
        vertex_color.data[0].color) != color if vertex_color.data else False

    # Change the vertex color, if necessary.
    if not set_color:
        return

    for data in vertex_color.data:
        data.color = color


def set_viewport_shading(context: Context, type: str, color_type: str) -> None:
    """Set the viewport shading to vertex color for the highlighting.

    Args:
        context (Context): The current Blender context.
        type (str): The shading type (Blender specific).
        color_type (str): The color type (Blender specific).
    """

    area = next(area for area in context.screen.areas if area.type == 'VIEW_3D')
    space = next(space for space in area.spaces if space.type == 'VIEW_3D')

    space.shading.type = type
    space.shading.color_type = color_type


def get_rendering_device(context: Context) -> str:
    """Get the device type used for rendering.

    Args:
        context (Context): The current Blender context.

    Returns:
        str: The used rendering device.
    """

    # Assume, that all other rendering engines
    # (the built-in ones should do) use the GPU for rendering.
    if context.scene.render.engine != "CYCLES":
        return "GPU"

    cycles_prefs = context.preferences.addons['cycles'].preferences

    # Determine, whether the rendering device is a CPU.
    is_cpu = context.scene.cycles.device == "CPU" or cycles_prefs.compute_device_type == "NONE"

    # Get a list of all enabled GPU and CPU devices.
    enabled_gpu_devices = list(filter(lambda x: x.use == 1, [
        dev for dev in cycles_prefs.devices if dev.type != "CPU"]))
    enabled_cpu_devices = list(filter(
        lambda x: x.use == 1, cycles_prefs.get_devices_for_type("CPU")))

    # Determine, in which combination GPU and/or CPU are turned on.
    device_combinations = [
        len(enabled_gpu_devices) > 0, len(enabled_cpu_devices) > 0]

    if is_cpu or device_combinations == [False, True]:
        return "CPU"

    if device_combinations == [True, True]:
        return "Hybrid"

    return "GPU"


def update_json101(path: str) -> dict:
    """Update the JSON data to version 1.0.1

    Args:
        path (str): The path to the JSON file.

    Returns:
        dict: The updated JSON data.
    """

    # Get the SEA data
    j = decode_json(path)

    # Update the dates_hours_alignment to use minutes instead of hours.
    for i in j["dates_hours_alignment"]:
        j["dates_hours_alignment"][i] = round(
            j["dates_hours_alignment"][i] * 60, 2)

    # Update the time values to use minutes instead of hours.
    j["time_yesterday"] = round(j["time_yesterday"] * 60, 2)
    j["time_today"] = round(j["time_today"] * 60, 2)

    # Update the file version number.
    j["check_update"] = 101

    # Save the SEA data.
    encode_json(j, path)

    return j


def update_json_and_data110(path: str) -> dict:
    """Update the JSON data to version 1.1.0

    Args:
        path (str): The path to the JSON file.

    Returns:
        dict: The updated JSON data.
    """

    # Decode the SEA data.
    j = decode_json(path)

    # Update the file version number.
    j["check_update"] = 110

    # Filenames of the DB files that should be deleted.
    db_filenames = ["Blender Analytics c704d36c50269763b8bce4479f.db",
                    "Blender Analytics e6017460ea3479e67886f3430845.db"]

    # Delete the DB files.
    for file in db_filenames:
        file = p.join(p.dirname(path), file)
        if p.exists(file):
            os.remove(file)

    # Save the SEA data.
    encode_json(j, path)

    return j


def update_json_and_data120(path: str) -> dict:
    """Update the JSON data to version 1.2.0

    Args:
        path (str): The path to the JSON file.

    Returns:
        dict: The updated JSON data.
    """

    FORMAT = "[%d, %m, %Y]"

    # Get the SEA data.
    j = decode_json(path)

    # Get the items of the dates_hours_alignment.
    elements = list(j["dates_hours_alignment"].keys())

    # Change the labels of the items.
    for i in elements:
        try:
            new_label = time.strftime("%Y-%m-%d", time.strptime(i, FORMAT))
        except Exception:
            continue
        j["dates_hours_alignment"][new_label] = j["dates_hours_alignment"].pop(
            i)

    j["rendering_devices"] = {
        "CPU": 0,
        "GPU": 0,
        "Hybrid": 0
    }

    # Change the format of start_time to be seconds since the epoch.
    j["start_time"] = 1581030000

    # Add the undo counter.
    j["undo_count"] = 0

    # Update the data version number.
    j["check_update"] = 120

    # Save the SEA data.
    encode_json(j, path)

    return j


def update_json(path: str) -> None:
    """Checks the version of the JSON Data file and updates, if necessary.

    Args:
        path (str): The path to the JSON file.
    """

    # Get the SEA data.
    j = decode_json(path)

    # Update the file to version 1.0.1
    if not "check_update" in j.keys():
        j = update_json101(path)

    # Update the file to version 1.1.0
    if j["check_update"] == 101:
        j = update_json_and_data110(path)

    # Update the file to version 1.2.0
    if j["check_update"] == 110:
        j = update_json_and_data120(path)
