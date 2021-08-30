import bpy

import os
from os import path as p

from .functions.mainFunctions import (
    date_unregister,
    get_yesterday,
    get_today,
    get_last_week,
    get_default_cubes
)


class SUPEREASYANALYTICS_PT_main(bpy.types.Panel):
    """Panel of the Super Easy Analytics Addon"""
    bl_category = "View"
    bl_idname = "SUPEREASYANALYTICS_PT_main"
    bl_label = "Super Easy Analytics"

    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        addon_prefs = context.preferences.addons[__package__].preferences

        # Path to the Super Easy Analytics Data.
        path = p.join(p.expanduser("~"),
                      "Blender Addons Data",
                      "blender-analytics",
                      "data.json")

        layout = self.layout

        # First, calculate the usage time.
        date_unregister(path)

        # Manipulate the time based on the display settings.
        if addon_prefs.display_unit:
            display_unit = "minutes"
            today = get_today(path)
            yesterday = get_yesterday(path)
            last_week = get_last_week(path)
        else:
            display_unit = "hours"
            today = round(get_today(path) / 60, 2)
            yesterday = round(get_yesterday(path) / 60, 2)
            last_week = round(get_last_week(path) / 60, 2)

        # Generic Display text.
        username = p.basename(p.expanduser("~"))
        layout.label(
            text=f"Hello {username}, here are your Super Easy Analytics:")

        layout.label(text="Blender Usage:", icon='TIME')

        # Blender Usage Display text.
        layout.label(
            text=f"Today, you've used Blender for {today} {display_unit}.")
        layout.label(
            text=f"Yesterday, you've used Blender for {yesterday} {display_unit}.")
        layout.label(
            text=f"During the last week, you've used Blender for {last_week} {display_unit}.")
        layout.label(text="")

        # Default Cubes Display text.
        layout.label(text="Default Cubes:", icon="MESH_CUBE")
        layout.label(
            text=f"You've deleted {get_default_cubes(path)} default cubes so far.")


classes = (
    SUPEREASYANALYTICS_PT_main,
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
