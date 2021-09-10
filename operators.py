import bpy
from bpy.props import (
    FloatProperty,
)
from os import path as p

from .functions.main_functions import (
    check_for_cube
)
from .functions.register_functions import (
    date_unregister
)

PATH = p.join(p.expanduser(
    "~"), "Blender Addons Data", "blender-analytics", "data.json")


class SUPEREASYANALYTICS_OT_modal(bpy.types.Operator):
    """Utility Operator that handles events in Blender."""
    bl_idname = "supereasyanalytics.modal"
    bl_label = "Operator"
    bl_options = {'REGISTER', 'UNDO'}

    def modal(self, context, event):
        if event.type in ["MOUSEMOVE", "INBETWEEN_MOUSEMOVE"]:
            return {"PASS_THROUGH"}

        if event.type == "WINDOW_DEACTIVATE":
            print("Deactivated Blender!")
            return {'PASS_THROUGH'}

        if event.type == "X":
            check_for_cube(context, bpy.data, PATH)

        date_unregister(PATH)

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


class SUPEREASYANALYTICS_OT_select_unapplied_scale(bpy.types.Operator):
    """Select all objects with unapplied scale. Excludes linked duplicates, because scale can't be applied on linked duplicates!"""
    bl_idname = "supereasyanalytics.select_unapplied_scale"
    bl_label = "Select objects with unapplied scale"
    bl_options = {'UNDO'}

    def execute(self, context):
        for ob in context.scene.objects:
            ob.select_set(False)
            ob_scale = (ob.scale.x, ob.scale.y, ob.scale.z)

            is_mesh = ob.type == "MESH"
            multi_user = False
            if is_mesh:
                multi_user = ob.data.users > 1

            if is_mesh and not multi_user and not ob_scale == (1.0, 1.0, 1.0):
                ob.select_set(True)

        return {'FINISHED'}


classes = (
    SUPEREASYANALYTICS_OT_modal,
    SUPEREASYANALYTICS_OT_save_reminder,
    SUPEREASYANALYTICS_OT_set_project_price,
    SUPEREASYANALYTICS_OT_select_unapplied_scale
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
