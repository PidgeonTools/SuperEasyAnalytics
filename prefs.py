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

import bpy
import os

from . import addon_updater_ops
from . import operators

from .functions.jsonFunctions import decode_json
from .functions.blenderdefender_functions import url


bl_info = {
    "name": "Blender Analytics",
    "author": "Blender Defender",
    "version": (1, 0, 0),
    "blender": (2, 83, 0),
    "location": "Sidebar (N) > View > Blender Analytics",
    "description": "Analyze your Blender behavior!",
    "warning": "Checkout Gumroad for other Addons and more...",
    "wiki_url": "https://gumroad.com/blenderdefender",
    "tracker_url": "https://github.com/BlenderDefender/Blender-Analytics/issues",
    "category": "Analytics"
}


class DemoPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    # addon updater preferences

    auto_check_update = bpy.props.BoolProperty(
        name="Auto-check for Update",
        description="If enabled, auto-check for updates using an interval",
        default=True,
    )
    updater_intrval_months = bpy.props.IntProperty(
        name='Months',
        description="Number of months between checking for updates",
        default=0,
        min=0
    )
    updater_intrval_days = bpy.props.IntProperty(
        name='Days',
        description="Number of days between checking for updates",
        default=7,
        min=0,
        max=31
    )
    updater_intrval_hours = bpy.props.IntProperty(
        name='Hours',
        description="Number of hours between checking for updates",
        default=0,
        min=0,
        max=23
    )
    updater_intrval_minutes = bpy.props.IntProperty(
        name='Minutes',
        description="Number of minutes between checking for updates",
        default=0,
        min=0,
        max=59
    )

    def draw(self, context):
        path = os.path.join(os.path.expanduser("~"), "Blender Addons Data", "blender-analytics")
        db_path = os.path.join(path, "Blender Analytics e6017460ea3479e67886f3430845.db")

        layout = self.layout

        if not os.path.exists(db_path):
            layout.label(text="One step left:")
            layout.label(text="Enter your license key (you should have received one via E-Mail) to make the Addon work.")
            layout.label(text="")
            layout.label(text="Don't worry, this addon is free forever.")
            layout.label(text="But in order for you to give advantages if you donated, we have to verify your purchase.")
            layout.operator("blender_analytics.license_key")
        else:
            data = decode_json(db_path)

            layout.label(text="Hello {}, here are your Addon Preferences:".format(data["purchase"]["How do you want to be called?"]))

            if data["purchase"]["price"] <= 0:
                layout.operator("wm.url_open", text="Checkout Gumroad for other addons and more...").url = "https://gumroad.com/blenderdefender"
                layout.label(text="Blender Analytics - You are using the free version.")
                layout.label(text="If you want to support me and get cool discount codes, please")
                layout.label(text="upgrade to donation version by purchasing again and leaving a tip. :)")
                layout.operator("wm.url_open", text="Upgrade", icon='FUND').url = "https://gumroad.com/l/BlenderAnalytics"
            elif data["purchase"]["price"] > 0:
                layout.label(text="Blender Analytics - You are using the donation version. Thank you :)", icon='FUND')
                layout.operator("wm.url_open", text="Get discount code for cool Blender Products").url=url()


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


classes = (
    DemoPreferences,
)


def register():
    # addon updater code and configurations
    # in case of broken version, try to register the updater first
    # so that users can revert back to a working version
    addon_updater_ops.register(bl_info)
    # operators.register()
    # register the example panel, to show updater buttons
    for cls in classes:
        addon_updater_ops.make_annotations(cls)  # to avoid blender 2.8 warnings
        bpy.utils.register_class(cls)


def unregister():
    # addon updater unregister
    addon_updater_ops.unregister()
    # operators.unregister()
    # register the example panel, to show updater buttons
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
