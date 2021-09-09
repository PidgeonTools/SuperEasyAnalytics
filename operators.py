import bpy
from bpy.props import (
    FloatProperty,
)
from os import path as p

from .functions.main_functions import (
    check_for_cube
)

PATH = p.join(p.expanduser(
    "~"), "Blender Addons Data", "blender-analytics", "data.json")


class SUPEREASYANALYTICS_OT_modal(bpy.types.Operator):
    """Utility Operator that handles events in Blender."""
    bl_idname = "supereasyanalytics.modal"
    bl_label = "Operator"
    bl_options = {'REGISTER', 'UNDO'}

    def modal(self, context, event):
        if event.type in ["MOUSEMOVE", "INBETWEEN_MOUSEMOVE", "LEFTMOUSE", "MIDDLEMOUSE", "RIGHMOUSE"]:
            return {"PASS_THROUGH"}

        if event.type == "WINDOW_DEACTIVATE":
            print("Deactivated Blender!")
            return {'PASS_THROUGH'}

        if event.type == "X":
            check_for_cube(context, bpy.data, PATH)

        return {'PASS_THROUGH'}

    def execute(self, context):
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


class SUPEREASYANALYTICS_OT_save_reminder(bpy.types.Operator):
    """Reminder: You need to save"""
    bl_idname = "supereasyanalytics.save_reminder"
    bl_label = "Save your file!"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.wm.save_mainfile('INVOKE_DEFAULT')

        return {'RUNNING_MODAL'}


class SUPEREASYANALYTICS_OT_set_project_price(bpy.types.Operator):
    """Set the price you get paid for this project."""
    bl_idname = "supereasyanalytics.set_project_price"
    bl_label = "Set Project Price"
    bl_options = {'UNDO'}

    price: FloatProperty(
        name="Project Price",
        default=0.0
    )

    def execute(self, context):
        context.scene.project_price = self.price

        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)


classes = (
    SUPEREASYANALYTICS_OT_modal,
    SUPEREASYANALYTICS_OT_save_reminder,
    SUPEREASYANALYTICS_OT_set_project_price
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
