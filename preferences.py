# This module contains user preference settings for this add-on.

import bpy
from bpy.types import AddonPreferences
from bpy.props import BoolProperty, IntProperty

ADDON_NAME = __package__

class AddonPreferences(AddonPreferences):
    bl_idname = ADDON_NAME

    beginner_help: BoolProperty(
        name="Beginner ToolTips",
        description="If on labels and buttons designed to help new users of this add-on will appear",
        default=True
    )

    experimental_features: BoolProperty(
        name="Experimental Features",
        description="If on, experiemental features will be shown in the add-ons user interface",
        default=False
    )

    save_imported_textures: BoolProperty(
        name="Save Imported Textures", 
        default=False,
        description="If on, all textures imported through operators in this add-on will be saved to an external folder named 'Raw Textures' next to the blend file. This helps manage texture files used in materials by keeping all of them in a constant location next to the blend file in which they are used."
    )

    auto_save_images: BoolProperty(
        name="Auto Save Images",
        default=False,
        description="(Requires Blender Restart) - If on, all images in the blend file that have defined paths, and require saving will be auto-saved at the defined interval."
    )

    image_auto_save_interval: IntProperty(
        name="Image Auto Save Interval",
        default=300,
        description="The interval in seconds for saving all images stored in the blend file"
    )

    log_main_operations: BoolProperty(
        name="Log Main Operations",
        default=True,
        description="If on, debug info for main functions ran by this add-on will be printed to Blenders terminal"
    )

    log_sub_operations: BoolProperty(
        name="Log Sub Processes",
        default=True,
        description="If on, debug info for secondary / smaller functions ran by this add-on will be printed to Blenders terminal"
    )

    thirty_two_bit: BoolProperty(
        name="32 Bit Color", 
        description="If on, images created using this add-on will be created with 32 bit color depth. 32-bit images will take up more memory, but will have significantly less color banding in gradients", 
        default=True
    )

    #----------------------------- ADDON PREFERENCE MENU -----------------------------#
    def draw(self, context):
        layout = self.layout

        # Draw texture management operations.
        layout.label(text="Texture Management")

        # Draw the raw texture folder preference.
        split = layout.split(factor=0.3)
        first_column = split.column()
        second_column = split.column()
        row = first_column.row()
        row.label(text="Raw Texture Folder")
        row = second_column.row(align=True)
        row.prop(bpy.context.scene, "matlayer_raw_textures_folder", text="")
        row.operator("matlayer.set_raw_texture_folder", text="", icon='FOLDER_REDIRECT')
        row.operator("matlayer.open_raw_texture_folder", text="", icon='FILE_FOLDER')

        # Draw the mesh map folder preference.
        row = first_column.row()
        row.label(text="Mesh Map Folder")
        row = second_column.row(align=True)
        row.prop(bpy.context.scene, "matlayer_mesh_map_folder", text="")
        row.operator("matlayer.set_mesh_map_folder", text="", icon='FOLDER_REDIRECT')
        row.operator("matlayer.open_mesh_map_folder", text="", icon='FILE_FOLDER')

        # Draw 32-bit color depth setting.
        layout.prop(self, "thirty_two_bit")
        layout.prop(self, "save_imported_textures")
        layout.prop(self, "auto_save_images")
        layout.prop(self, "image_auto_save_interval")

        # Draw debug logging preferences.
        layout.label(text="Debug Logging")
        layout.prop(self, "log_main_operations")
        layout.prop(self, "log_sub_operations")

        # Draw other preferences.
        layout.label(text="Other")
        layout.prop(self, "beginner_help")
        layout.prop(self, "experimental_features")