import bpy

from os import path as p

from .functions.main_functions import (
    date_unregister
)


class SUPEREASYANALYTICS_HT_count_project_time(bpy.types.Header):
    bl_label = "Calculate the time spent on this project"
    bl_space_type = "STATUSBAR"
    #bl_region_type = "HEADER"

    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        # Path to the Super Easy Analytics Data.
        path = p.join(p.expanduser("~"),
                      "Blender Addons Data",
                      "blender-analytics",
                      "data.json")
        date_unregister(path)


classes = (
    SUPEREASYANALYTICS_HT_count_project_time,
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
