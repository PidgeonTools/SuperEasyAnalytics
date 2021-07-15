import bpy

import os
from os import path as p

from .functions.mainFunctions import (
    date_unregister,
    get_yesterday,
    get_today,
    get_default_cubes
)


class Blender_Analytics_PT_main(bpy.types.Panel):
    """Panel of the Blender Analytics Addon"""
    bl_category = "View"
    bl_idname = "Blender_Analytics_PT_main"
    bl_label = "Blender Analytics"

    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        addon_prefs = context.preferences.addons[__package__].preferences

        # Path to the Blender Analytics Data.
        path = p.join(p.expanduser("~"),
                      "Blender Addons Data",
                      "blender-analytics",
                      "data.json")

        layout = self.layout

        # First, calculate the usage time.
        date_unregister(path)

        # Manipulate the time based on the display settings.
        if addon_prefs.display_unit:
            today = str(get_today(path)) + " minutes."
            yesterday = str(get_yesterday(path)) + " minutes."
        else:
            today = str(round(get_today(path) / 60, 2)) + " hours."
            yesterday = str(round(get_yesterday(path) / 60, 2)) + " hours."

        # Generic Display text.
        username = p.basename(p.expanduser("~"))
        layout.label(
            text=f"Hello {username}, here are your Blender Analytics:")

        layout.label(text="Blender Usage:", icon='BLENDER')

        # Blender Usage Display text.
        layout.label(text=f"Today, you've used Blender for {today}")
        layout.label(text=f"Yesterday, you've used Blender for {yesterday}")
        layout.label(text="")

        # Default Cubes Display text.
        layout.label(text="Default Cubes:", icon="MESH_CUBE")
        layout.label(
            text=f"You've deleted {get_default_cubes(path)} default cubes so far.")


classes = (
    Blender_Analytics_PT_main,
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
