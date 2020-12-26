import bpy
import os

import requests
import json

from .functions.jsonFunctions import decode_json, encode_json


class BLENDERANALYTICS_OT_verify_license(bpy.types.Operator):
    """Upgrade from free to donation version"""
    bl_idname = "blender_analytics.license_key"
    bl_label = "Enter your License Key"

    license_key = bpy.props.StringProperty(
    name='License Key',
    description="Enter the license key you received via E-Mail",
    default=""
    )

    def execute(self, context):
        """Enter your license key"""
        key = self.license_key

        path = os.path.join(os.path.expanduser("~"), "Blender Addons Data", "blender-analytics")
        db_path = os.path.join(path, "Blender Analytics e6017460ea3479e67886f3430845.db")

        try:
            with open(os.path.join(path, "Blender Analytics c704d36c50269763b8bce4479f.db"), "w+") as f:
                f.write(key)

            permalink = "BlenderAnalytics"
            data = json.loads(requests.post("https://api.gumroad.com/v2/licenses/verify",
                                            data={"product_permalink": permalink,
                                                  "license_key": key,
                                                  "increment_uses_count": "true"}).text)
            if data["success"]:
                encode_json(data, db_path)
                self.report({"INFO"}, "Successfully registered your license key! Please restart Blender to use this addon.")
            else:
                self.report({"WARNING"}, "Your license key is invalid! Please try again.")

        except:
            self.report({"WARNING"}, "Please connect with the internet and try again!")

        return{"FINISHED"}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "license_key")
        layout.label(text="Please enter your License Key.")
        layout.label(text="Don't worry, the addon is free and remains free forever!")

classes = (
     BLENDERANALYTICS_OT_verify_license,
)

def register():

    # register the example panel, to show updater buttons
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():

    # register the example panel, to show updater buttons
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)