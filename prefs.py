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

from bpy.props import (
    BoolProperty,
    FloatProperty,
    IntProperty
)
from bpy.utils import (
    register_class,
    unregister_class
)
from bpy.types import (
    AddonPreferences,
    Context,
    UILayout
)

from os import path as p

from . import addon_updater_ops


class SUPEREASYANALYTICS_APT_Preferences(AddonPreferences):
    bl_idname = __package__

    # addon updater preferences
    auto_check_update: BoolProperty(
        name="Auto-check for Update",
        description="If enabled, auto-check for updates using an interval",
        default=True,
    )
    updater_intrval_months: IntProperty(
        name='Months',
        description="Number of months between checking for updates",
        default=0,
        min=0
    )
    updater_intrval_days: IntProperty(
        name='Days',
        description="Number of days between checking for updates",
        default=7,
        min=0,
        max=31
    )
    updater_intrval_hours: IntProperty(
        name='Hours',
        description="Number of hours between checking for updates",
        default=0,
        min=0,
        max=23
    )
    updater_intrval_minutes: IntProperty(
        name='Minutes',
        description="Number of minutes between checking for updates",
        default=0,
        min=0,
        max=59
    )

    display_unit: BoolProperty(
        name="Display Unit",
        description="Switch between displaying in minutes or in hours",
        default=True
    )

    freelancer_stats: BoolProperty(
        name="Freelancer Statistics",
        description="Enable a set of statistics, that can be useful to freelancers.",
        default=False
    )

    save_reminder_interval: FloatProperty(
        name="Save Reminder Interval",
        description="Number of minutes until reminding you to save.",
        min=0.0,
        default=5.0
    )

    auto_save: BoolProperty(
        name="Automatically save files",
        description="Save the current file automatically (instead of showing the save reminder)",
        default=False
    )

    system_memory: IntProperty(
        name="System RAM",
        description="The amount of RAM that you have available in your system.",
        default=8192,
        step=1024
    )

    def draw(self, context: Context):
        layout: UILayout = self.layout

        # Get the username of the logged in user.
        username = p.basename(p.expanduser("~"))
        layout.label(
            text=f"Hello {username}, here are your Addon Preferences:")

        # Layout the setting for the display unit.
        layout.label(text="Display unit:")
        if self.display_unit:
            layout.prop(self, "display_unit", toggle=True,
                        text="Active Display Unit: Minutes")
        else:
            layout.prop(self, "display_unit", toggle=True,
                        text="Active Display Unit: Hours")

        # Layout the save reminder interval setting.
        layout.separator(factor=0.5)
        layout.label(text="Save Reminder:")
        layout.prop(self, "save_reminder_interval")
        layout.prop(self, "auto_save")

        # System RAM
        layout.separator(factor=0.5)
        layout.label(text="System preferences:")
        layout.prop(self, "system_memory")

        # Layout the setting for turning the freelancer stats on / off.
        layout.separator(factor=0.5)
        layout.label(text="Optional Statistics:")
        layout.prop(self, "freelancer_stats",
                    text="Enable Freelancer Statistics")

        # col = layout.column() # works best if a column, or even just self.layout
        mainrow = layout.row()
        col = mainrow.column()

        # updater draw function
        # could also pass in col as third arg
        addon_updater_ops.update_settings_ui(self, context)

        # Alternate draw function, which is more condensed and can be
        # placed within an existing draw function. Only contains:
        #   1) check for update/update now buttons
        #   2) toggle for auto-check (interval will be equal to what is set above)
        # addon_updater_ops.update_settings_ui_condensed(self, context, col)

        # Adding another column to help show the above condensed ui as one column
        # col = mainrow.column()
        # col.scale_y = 2
        # col.operator("wm.url_open","Open webpage ").url=addon_updater_ops.updater.website

        # Layout the discord URL.
        col = layout.column()
        op = col.operator("wm.url_open", text="Support", icon="URL")
        op.url = "https://bd-links.netlify.app/discord-sea"


classes = (
    SUPEREASYANALYTICS_APT_Preferences,
)


def register(bl_info):
    # addon updater code and configurations
    # in case of broken version, try to register the updater first
    # so that users can revert back to a working version
    addon_updater_ops.register(bl_info)
    # register the example panel, to show updater buttons
    for cls in classes:
        addon_updater_ops.make_annotations(
            cls)  # to avoid blender 2.8 warnings
        register_class(cls)


def unregister():
    # addon updater unregister
    addon_updater_ops.unregister()
    # register the example panel, to show updater buttons
    for cls in reversed(classes):
        unregister_class(cls)
