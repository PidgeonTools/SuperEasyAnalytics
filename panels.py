import bpy
import os

from .functions.mainFunctions import (
    check_for_cube,
    date_register,
    date_unregister,
    get_yesterday,
    get_today,
    get_default_cubes
)
from .functions.jsonFunctions import decode_json


class Blender_Analytics_PT_main(bpy.types.Panel):
    """Panel of the Blender Analytics Addon"""
    bl_category = "View"
    bl_idname = "Blender_Analytics_PT_main"
    bl_label = "Blender Analytics"

    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):

        path = os.path.join(os.path.expanduser("~"),
                            "Blender Addons Data",
                            "blender-analytics",
                            "data.json")
        db_path = os.path.join(os.path.dirname(path), "Blender Analytics e6017460ea3479e67886f3430845.db")

        layout = self.layout
        date_unregister(path)
        data = decode_json(db_path)

        layout.label(text="Hello {}, here are your Blender Analytics:".format(data["purchase"]["How do you want to be called?"]))
        layout.label(text="Blender Usage:", icon='BLENDER')
        layout.label(text="Today, you've used Blender for {} hours".format(get_today(path)))
        layout.label(text="Yesterday, you've used Blender for {} hours".format(get_yesterday(path)))
        layout.label(text="")
        layout.label(text="Default Cubes:", icon="MESH_CUBE")
        layout.label(text="You've deleted {} default cubes so far.".format(get_default_cubes(path)))


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
