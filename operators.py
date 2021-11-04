import bpy
from bpy.props import (
    BoolProperty,
    FloatProperty,
    IntProperty,
)
from bpy.types import (
    Context,
    Event,
    Operator
)
from bpy.utils import (
    register_class,
    unregister_class
)


from os import path as p

from .functions.main_functions import (
    check_for_cube,
    highlight_object,
    set_viewport_shading
)
from .functions.register_functions import (
    date_unregister
)

PATH = p.join(p.expanduser(
    "~"), "Blender Addons Data", "blender-analytics", "data.json")


class SUPEREASYANALYTICS_OT_modal(Operator):
    """Utility Operator that handles events in Blender."""
    bl_idname = "supereasyanalytics.modal"
    bl_label = "Operator"
    bl_options = {'REGISTER', 'UNDO'}

    def modal(self, context: Context, event: Event):
        # Do nothing, if only the mouse is moved.
        if event.type in ["MOUSEMOVE", "INBETWEEN_MOUSEMOVE"]:
            return {"PASS_THROUGH"}

        # Do nothing, if Blender is deactivated.
        if event.type == "WINDOW_DEACTIVATE":
            print("Deactivated Blender!")  # Debugging only
            return {'PASS_THROUGH'}

        # Check, if the default cube was deleted, if X is pressed (? TODO: Is this necessary ?)
        if event.type == "X":
            show_graveyard_animation = check_for_cube(context, bpy.data, PATH)

        # Update the time counter.
        date_unregister(PATH)

        return {'PASS_THROUGH'}

    def execute(self, context: Context):
        # Start the modal Operation.
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


class SUPEREASYANALYTICS_OT_save_reminder(Operator):
    """Reminder: You need to save"""
    bl_idname = "supereasyanalytics.save_reminder"
    bl_label = "Save your file!"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context: Context):
        # Save the current file. Show the file dialog, if the file isn't saved anywhere.
        bpy.ops.wm.save_mainfile('INVOKE_DEFAULT')

        return {'RUNNING_MODAL'}


class SUPEREASYANALYTICS_OT_set_project_price(Operator):
    """Set the price you get paid for this project."""
    bl_idname = "supereasyanalytics.set_project_price"
    bl_label = "Set Project Price"
    bl_options = {'UNDO'}

    price: FloatProperty(
        name="Project Price",
        default=0.0
    )

    def execute(self, context: Context):
        context.scene.project_price = self.price

        return {'FINISHED'}

    def invoke(self, context: Context, event: Event):
        return context.window_manager.invoke_props_dialog(self)


class SUPEREASYANALYTICS_OT_highlight_unapplied_scale(Operator):
    """Select all objects with unapplied scale. Linked duplicates are highlighted with a color, but not selected, because scale can't be applied on linked duplicates"""
    bl_idname = "supereasyanalytics.highlight_unapplied_scale"
    bl_label = "Highlight objects with unapplied scale"
    bl_options = {'UNDO'}

    def execute(self, context: Context):
        for ob in context.scene.objects:
            ob.select_set(False)
            ob_scale = (ob.scale.x, ob.scale.y, ob.scale.z)

            # Abort, if the current object is not a mesh.
            if not ob.type == "MESH":
                continue

            # Check, if the object has unapplied scale
            # and is not a multi user and select it, if that's the case.
            select = ob_scale != (1.0, 1.0, 1.0)
            if not ob.data.users > 1 and select:
                ob.select_set(True)

            # Shade the object in a color according to the result of the operation.
            highlight_object(ob, select)

        # Change the viewport shading to vertex color.
        set_viewport_shading(context, "SOLID", "VERTEX")
        return {'FINISHED'}


class SUPEREASYANALYTICS_OT_highlight_flat_shaded(Operator):
    """Highlight all objects that are not smooth-shaded"""
    bl_idname = "supereasyanalytics.highlight_flat_shaded"
    bl_label = "Highlight objects that are not smooth-shaded."
    bl_options = {'UNDO'}

    def execute(self, context: Context):
        for ob in context.scene.objects:
            ob.select_set(False)

            # Abort, if the current object is not a mesh.
            if not ob.type == "MESH":
                continue

            # Check, if the current object is flat shaded and select it, if that's the case.
            shade_flat = False in [pol.use_smooth for pol in ob.data.polygons]
            if shade_flat:
                ob.select_set(True)
                context.view_layer.objects.active = ob

            # Highlight the object according to whether it's flat shaded or not.
            highlight_object(ob, shade_flat)

        # Change the viewport shading to vertex color.
        set_viewport_shading(context, "SOLID", "VERTEX")

        return {'FINISHED'}


class SUPEREASYANALYTICS_OT_highlight_hidden_objects(Operator):
    """Highlight all objects that are hidden but will be visible, when rendering"""
    bl_idname = "supereasyanalytics.highlight_hidden_objects"
    bl_label = "Highlight hidden objects that will be visible when rendering."
    bl_options = {'REGISTER', 'UNDO'}

    def modal(self, context: Context, event: Event):
        # Keep the operator running, if the person only navigates.
        if event.type in ["MOUSEMOVE", "INBETWEEN_MOUSEMOVE", "WINDOW_DEACTIVATE", "WHEELDOWNMOUSE", 'WHEELUPMOUSE', 'MIDDLEMOUSE', 'RIGHT_SHIFT', 'LEFT_SHIFT']:
            return {"PASS_THROUGH"}

        # Hide all objects that were hidden previously.
        for ob in self.hidden_objects:
            ob.hide_set(True)

        return {'FINISHED'}

    def execute(self, context: Context):
        self.hidden_objects = []

        for ob in context.scene.objects:
            ob.select_set(False)

            # Check, if the object is hidden, but visible when rendering.
            hidden = not ob.hide_render and ob.hide_get()
            if hidden:
                ob.hide_set(False)
                ob.select_set(True)
                self.hidden_objects.append(ob)

            # Highlight the object based on whether it's hidden or not.
            highlight_object(ob, hidden)

        # Change the viewport shading to vertex color.
        set_viewport_shading(context, "SOLID", "VERTEX")

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


class SUPEREASYANALYTICS_OT_highlight_objects_without_material(Operator):
    """Highlight all objects that do not have a material assigned to them"""
    bl_idname = "supereasyanalytics.highlight_objects_without_material"
    bl_label = "Highlight objects without material"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context: Context):
        for ob in context.scene.objects:
            ob.select_set(False)

            # Abort, if the current object is not a mesh.
            if not ob.type == "MESH":
                continue

            # Check, if the object has a material assigned to it.
            has_no_material = True
            for slot in ob.material_slots:
                if slot.material != None:
                    has_no_material = False
                    break

            if has_no_material:
                ob.select_set(True)

            # Highlight the object based on whether it has a material or not.
            highlight_object(ob, has_no_material)

        # Change the viewport shading to vertex color.
        set_viewport_shading(context, "SOLID", "VERTEX")

        return {'FINISHED'}


class SUPEREASYANALYTICS_OT_highlight_non_manifold(Operator):
    """Highlight all objects that are non-manifold"""
    bl_idname = "supereasyanalytics.highlight_non_manifold"
    bl_label = "Highlight Non-Manifold objects"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context: Context):

        for ob in context.scene.objects:
            ob.select_set(False)

            # Abort, if the current object is not a mesh.
            if not ob.type == "MESH":
                continue

            # Select the object and switch to Edit Mode.
            context.view_layer.objects.active = ob
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_mode(type="VERT")

            # Select all vertecies, if at least one vertex is selected.
            if context.active_object.data.total_vert_sel > 0:
                bpy.ops.mesh.select_all()

            # Make use of the select_non_manifold() function.
            bpy.ops.mesh.select_non_manifold()

            # Determine, whether the object is non-manifold.
            non_manifold = False
            if context.active_object.data.total_vert_sel > 0:
                non_manifold = True

            # Switch back to object mode.
            bpy.ops.object.mode_set(mode='OBJECT')

            # Highlight/select the object based on whether it is Non-Manifold or not.
            ob.select_set(non_manifold)
            highlight_object(ob, non_manifold)

        # Change the viewport shading to vertex color.
        set_viewport_shading(context, "SOLID", "VERTEX")

        return {'FINISHED'}


class SUPEREASYANALYTICS_OT_highlight_ngons(Operator):
    """Highlight all objects that have N-Gons."""
    bl_idname = "supereasyanalytics.highlight_ngons"
    bl_label = "Highlight N-Gon objects"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context: Context):

        for ob in context.scene.objects:
            ob.select_set(False)

            # Abort, if the current object is not a mesh.
            if not ob.type == "MESH":
                continue

            # Determine, whether the object has N-Gons.
            has_ngons = False
            for pol in ob.data.polygons:
                if len(pol.vertices) > 4:
                    has_ngons = True
                    ob.select_set(True)
                    break

            # Highlight/select the object based on whether it has N-Gons or not.
            highlight_object(ob, has_ngons)

        # Change the viewport shading to vertex color.
        set_viewport_shading(context, "SOLID", "VERTEX")

        return {'FINISHED'}


class SUPEREASYANALYTICS_OT_linked_duplicates_list(Operator):
    """List all linked duplicates."""
    bl_idname = "supereasyanalytics.linked_duplicates_list"
    bl_label = "List linked duplicates"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context: Context):
        D = bpy.data

        bpy.linked_duplicates = []

        for mesh in D.meshes:
            if mesh.users > 1:
                bpy.linked_duplicates.append(mesh)

        return {'FINISHED'}


class SUPEREASYANALYTICS_OT_unlink_duplicates(Operator):
    """Unlink a group of linked duplikates."""
    bl_idname = "supereasyanalytics.unlink_duplicates"
    bl_label = "Unlink Duplicates"
    bl_options = {'UNDO'}

    index: IntProperty(
        name="List index"
    )

    apply_scale: BoolProperty(
        name="Apply scale",
        default=False
    )

    def execute(self, context: Context):
        name = bpy.linked_duplicates[self.index].name

        for ob in bpy.data.objects:
            ob.select_set(False)
            if ob.data.name == name:
                ob.select_set(True)

        bpy.ops.object.make_single_user(
            object=True, obdata=True, material=False, animation=True)

        if self.apply_scale:
            bpy.ops.object.transform_apply(
                location=False, rotation=False, scale=True)

        bpy.linked_duplicates.pop(self.index)

        return {'FINISHED'}


classes = (
    SUPEREASYANALYTICS_OT_modal,
    SUPEREASYANALYTICS_OT_save_reminder,
    SUPEREASYANALYTICS_OT_set_project_price,
    SUPEREASYANALYTICS_OT_highlight_unapplied_scale,
    SUPEREASYANALYTICS_OT_highlight_flat_shaded,
    SUPEREASYANALYTICS_OT_highlight_hidden_objects,
    SUPEREASYANALYTICS_OT_highlight_objects_without_material,
    SUPEREASYANALYTICS_OT_highlight_non_manifold,
    SUPEREASYANALYTICS_OT_highlight_ngons,
    SUPEREASYANALYTICS_OT_linked_duplicates_list,
    SUPEREASYANALYTICS_OT_unlink_duplicates
)


def register():
    for cls in classes:
        register_class(cls)


def unregister():
    for cls in reversed(classes):
        unregister_class(cls)
