import bpy
from bpy.types import Panel

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


class SUPEREASYANALYTICS_PT_main(Panel):
    """Panel of the Super Easy Analytics Addon"""
    bl_category = "View"
    bl_idname = "SUPEREASYANALYTICS_PT_main"
    bl_label = "Super Easy Analytics"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        # Path to the Super Easy Analytics Data.
        path = p.join(p.expanduser("~"),
                      "Blender Addons Data",
                      "blender-analytics",
                      "data.json")

        layout = self.layout

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

    def draw(self, context):
        prefs = context.preferences.addons[__package__].preferences

        # Path to the Super Easy Analytics Data.
        path = p.join(p.expanduser("~"),
                      "Blender Addons Data",
                      "blender-analytics",
                      "data.json")

        layout = self.layout

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

    def draw(self, context):
        layout = self.layout

        layout.operator("supereasyanalytics.select_unapplied_scale", text="Highlight unapplied scale")


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

    def draw(self, context):
        prefs = context.preferences.addons[__package__].preferences

        price_per_hour = round(
            (context.scene.project_price / (bpy.project_time + 1)) * 60 * 60, 2)

        # Limit the price per hour display to start after 10 minutes
        # (the price per hour values are way too high after just a few seconds)
        if price_per_hour > context.scene.project_price * 6:
            price_per_hour = context.scene.project_price * 6

        layout = self.layout
        if context.scene.project_price == 0:
            layout.operator("supereasyanalytics.set_project_price")

        layout.label(
            text=f"At your current working time, you're getting paid ${price_per_hour} per hour.")


class SUPEREASYANALYTICS_PT_project_stats(Panel):
    """Statistics for the current project"""
    bl_label = "Project Statistics"
    bl_idname = "SUPEREASYANALYTICS_PT_project_stats"

    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_parent_id = "SUPEREASYANALYTICS_PT_main"

    def draw(self, context):
        prefs = context.preferences.addons[__package__].preferences

        layout = self.layout

        # Manipulate the time based on the display settings.
        if prefs.display_unit:
            display_unit = "minutes"
            project_time = round(bpy.project_time / 60)
        else:
            display_unit = "hours"
            project_time = round(bpy.project_time / (60 * 60))

        layout.label(
            text=f"You have spent {project_time} {display_unit} on this file so far.")


def save_reminder(self, context):
    layout = self.layout

    D = bpy.data

    prefs = context.preferences.addons[__package__].preferences
    remind = prefs.save_reminder_interval * 60 <= int(
        time.time()) - context.scene.save_timestamp

    if not D.is_saved or (D.is_dirty and remind):
        layout.operator("supereasyanalytics.save_reminder", icon="ERROR")


classes = (
    SUPEREASYANALYTICS_PT_main,
    SUPEREASYANALYTICS_PT_usage_stats,
    SUPEREASYANALYTICS_PT_scene_analytics,
    SUPEREASYANALYTICS_PT_freelancer_stats,
    SUPEREASYANALYTICS_PT_project_stats
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    bpy.types.VIEW3D_HT_header.append(save_reminder)


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    bpy.types.VIEW3D_HT_header.remove(save_reminder)
