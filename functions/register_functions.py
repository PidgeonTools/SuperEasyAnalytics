import bpy
from bpy.props import (
    BoolProperty,
    FloatProperty,
    StringProperty
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
