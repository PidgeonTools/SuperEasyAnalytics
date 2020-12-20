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
import queue
from mathutils import *

from . mainFunctions import (
    check_for_cube,
    date_register,
    date_unregister,
    get_yesterday,
    get_today,
    get_default_cubes
)

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
    "category": "Analytics"}
}

class Blender_Analytics_PT_main(bpy.types.Panel):
    """Panel of the Blender Analytics Addon"""
    bl_category = "View"
    bl_idname = "Blender_Analytics_PT_main"
    bl_label = "Blender Analytics"
    
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'


    def draw(self, context):
        layout = self.layout
        date_unregister()
        layout.label(text= "Blender Usage:", icon = 'BLENDER')
        layout.label(text= "Today, you've used Blender for {} hours".format(get_today()))
        layout.label(text= "Yesterday, you've used Blender for {} hours".format(get_yesterday()))
        layout.label(text= "")
        layout.label(text= "Default Cubes:", icon="MESH_CUBE")
        layout.label(text= "You've deleted {} default cubes so far.".format(get_default_cubes()))

classes = (
    Blender_Analytics_PT_main,
)


def register():
    global t 
    t = queue.threading.Timer(40, lambda: check_for_cube(bpy.data.meshes['Cube'].users))
    t.start()

    date_register()

    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)



def unregister():
    t.cancel()
    date_unregister()

    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
