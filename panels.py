import bpy
from bpy.types import (
    Context,
    Panel,
    UILayout
)
from bpy.utils import (
    register_class,
    unregister_class
)

import os
from os import path as p

import time

from .functions.main_functions import (
    get_yesterday,
    get_today,
    get_last_week,
    get_default_cubes,
    get_undos
)

from .functions.register_functions import (
    date_unregister
)

from .operators import (
    SUPEREASYANALYTICS_OT_highlight_unapplied_scale,
    SUPEREASYANALYTICS_OT_highlight_flat_shaded,
    SUPEREASYANALYTICS_OT_highlight_hidden_objects,
    SUPEREASYANALYTICS_OT_set_project_price,
    SUPEREASYANALYTICS_OT_save_reminder,
    SUPEREASYANALYTICS_OT_highlight_objects_without_material
)


class SUPEREASYANALYTICS_PT_main(Panel):
    """Panel of the Super Easy Analytics Addon"""
    bl_category = "View"
    bl_idname = "SUPEREASYANALYTICS_PT_main"
    bl_label = "Super Easy Analytics"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context: Context):
        # Path to the Super Easy Analytics Data.
        path = p.join(p.expanduser("~"),
                      "Blender Addons Data",
                      "blender-analytics",
                      "data.json")

        layout: UILayout = self.layout

        # First, calculate the usage time.
        date_unregister(path)

        # Generic Display text.
        username = p.basename(p.expanduser("~"))
        layout.label(
            text=f"Hello {username}, here are your Super Easy Analytics:")


class SUPEREASYANALYTICS_PT_usage_stats(Panel):
    """Usage Statistics"""
    bl_label = "Usage Statistics"
    bl_idname = "SUPEREASYANALYTICS_PT_usage_stats"

    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_parent_id = "SUPEREASYANALYTICS_PT_main"

    def draw(self, context: Context):
        prefs = context.preferences.addons[__package__].preferences

        # Path to the Super Easy Analytics Data.
        path = p.join(p.expanduser("~"),
                      "Blender Addons Data",
                      "blender-analytics",
                      "data.json")

        layout: UILayout = self.layout

        # Manipulate the time based on the display settings.
        if prefs.display_unit:
            display_unit = "minutes"
            today = get_today(path)
            yesterday = get_yesterday(path)
            last_week = get_last_week(path)
        else:
            display_unit = "hours"
            today = round(get_today(path) / 60, 2)
            yesterday = round(get_yesterday(path) / 60, 2)
            last_week = round(get_last_week(path) / 60, 2)

        layout.label(text="Blender Usage:", icon='TIME')

        # Blender Usage Display text.
        layout.label(
            text=f"Today, you've used Blender for {today} {display_unit}.")
        layout.label(
            text=f"Yesterday, you've used Blender for {yesterday} {display_unit}.")
        layout.label(
            text=f"During the last week, you've used Blender for {last_week} {display_unit}.")
        layout.label(text="")
        layout.label(
            text=f"While using Blender, you've undone {get_undos(path)} steps.")
        layout.label(text="")

        # Default Cubes Display text.
        layout.label(text="Default Cubes:", icon="MESH_CUBE")
        layout.label(
            text=f"You've deleted {get_default_cubes(path)} default cubes so far.")
        layout.label(text="")

        layout.label(text="App Statistics:", icon='BLENDER')

        # Blender App Stats.
        layout.label(
            text=f"You have {len(context.preferences.addons)} addons enabled.")


class SUPEREASYANALYTICS_PT_scene_analytics(Panel):
    """Analyze your current scene and highlight objects that fulfill certain criteria"""
    bl_label = "Scene Analytics"
    bl_idname = "SUPEREASYANALYTICS_PT_scene_analytics"

    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_parent_id = "SUPEREASYANALYTICS_PT_main"

    def draw(self, context: Context):
        layout: UILayout = self.layout

        layout.operator(SUPEREASYANALYTICS_OT_highlight_unapplied_scale.bl_idname,
                        text="Highlight unapplied scale")
        layout.operator(SUPEREASYANALYTICS_OT_highlight_flat_shaded.bl_idname,
                        text="Highlight flat shaded objects")
        layout.operator(SUPEREASYANALYTICS_OT_highlight_hidden_objects.bl_idname,
                        text="Highlight hidden objects that will be rendered.")  # ,
        # icon="RESTRICT_RENDER_OFF")  # TODO: Add icon or not?
        layout.operator(
            SUPEREASYANALYTICS_OT_highlight_objects_without_material.bl_idname)


class SUPEREASYANALYTICS_PT_freelancer_stats(Panel):
    """Freelancer Statistics"""
    bl_label = "Freelancer Statistics"
    bl_idname = "SUPEREASYANALYTICS_PT_freelancer_stats"

    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_parent_id = "SUPEREASYANALYTICS_PT_main"

    @classmethod
    def poll(cls, context):
        return context.preferences.addons[__package__].preferences.freelancer_stats

    def draw(self, context: Context):
        layout: UILayout = self.layout

        price_per_hour = round(
            (context.scene.project_price / (bpy.project_time + 1)) * 60 * 60, 2)

        # Limit the price per hour display to start after 10 minutes
        # (the price per hour values are way too high after just a few seconds)
        if price_per_hour > context.scene.project_price * 6:
            price_per_hour = context.scene.project_price * 6

        # Give the option to set the project price, if it is not set.
        if context.scene.project_price == 0:
            layout.operator(SUPEREASYANALYTICS_OT_set_project_price.bl_idname)

        # Layout the Price per hour.
        layout.label(
            text=f"At your current working time, you're getting paid ${price_per_hour} per hour.")


class SUPEREASYANALYTICS_PT_project_stats(Panel):
    """Statistics for the current project"""
    bl_label = "Project Statistics"
    bl_idname = "SUPEREASYANALYTICS_PT_project_stats"

    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_parent_id = "SUPEREASYANALYTICS_PT_main"

    def draw(self, context: Context):
        prefs = context.preferences.addons[__package__].preferences

        layout: UILayout = self.layout

        # Manipulate the time based on the display settings.
        if prefs.display_unit:
            display_unit = "minutes"
            project_time = round(bpy.project_time / 60)
            render_time = round(context.scene.render_time / 60)
        else:
            display_unit = "hours"
            project_time = round(bpy.project_time / (60 * 60))
            render_time = round(context.scene.render_time / (60 * 60))

        # Layout the scene statistics.
        layout.label(
            text=f"You have spent {project_time} {display_unit} on this file so far.")
        layout.label(
            text=f"You have spent {render_time} {display_unit} for rendering this file.")


def save_reminder(self, context):
    D = bpy.data

    prefs = context.preferences.addons[__package__].preferences

    layout: UILayout = self.layout

    # Determine, whether to remind the user of saving the file.
    remind = prefs.save_reminder_interval * 60 <= int(
        time.time()) - context.scene.save_timestamp

    # Display the reminder, if the file has unsaved changes and remind is True.
    if not D.is_saved or (D.is_dirty and remind):
        layout.operator(
            SUPEREASYANALYTICS_OT_save_reminder.bl_idname, icon="ERROR")


classes = (
    SUPEREASYANALYTICS_PT_main,
    SUPEREASYANALYTICS_PT_usage_stats,
    SUPEREASYANALYTICS_PT_scene_analytics,
    SUPEREASYANALYTICS_PT_freelancer_stats,
    SUPEREASYANALYTICS_PT_project_stats
)


def register():
    for cls in classes:
        register_class(cls)

    bpy.types.VIEW3D_HT_header.append(save_reminder)


def unregister():
    for cls in reversed(classes):
        unregister_class(cls)

    bpy.types.VIEW3D_HT_header.remove(save_reminder)
