import bpy


class SUPEREASYANALYTICS_OT_save_reminder(bpy.types.Operator):
    """Reminder: You need to save"""
    bl_idname = "supereasyanalytics.save_reminder"
    bl_label = "Save your file!"
    bl_options = {'REGISTER', 'UNDO'}

    def modal(self, context, event):
        prefs = context.preferences.addons[__package__].preferences

        if event.type == 'TIMER':
            prefs.display_reminder = True
            self.cancel(context)

        return {'PASS_THROUGH'}

    def execute(self, context):
        prefs = context.preferences.addons[__package__].preferences
        wm = context.window_manager

        bpy.ops.wm.save_mainfile('INVOKE_DEFAULT')

        prefs.display_reminder = False

        self._timer = wm.event_timer_add(
            60 * prefs.save_reminder_interval, window=context.window)
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)


classes = (
    SUPEREASYANALYTICS_OT_save_reminder,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    bpy.context.preferences.addons[__package__].preferences.display_reminder = True
