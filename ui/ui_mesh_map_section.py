# This files handles drawing baking section user interface.

import bpy
from .import ui_section_tabs
from ..core import mesh_map_baking
from ..core import blender_addon_utils
from .. import preferences


def draw_mesh_map_status(layout, addon_preferences):
    '''Draws status and operators for each mesh map type.'''
    layout.label(text="MESH MAPS")

    split = layout.split(factor=0.4)
    first_column = split.column()
    second_column = split.column()

    null_meshmap_text = "Not Baked"

    for mesh_map_type in mesh_map_baking.MESH_MAP_TYPES:
        mesh_map_label = mesh_map_type.replace('_', ' ')
        mesh_map_label = blender_addon_utils.capitalize_by_space(mesh_map_label)

        bake_checkbox_property_name = "bake_{0}".format(mesh_map_type.lower())
        row = first_column.row()
        row.prop(addon_preferences, bake_checkbox_property_name, text="")
        row.label(text=mesh_map_label)

        row = second_column.row()
        col = row.column()

        if bpy.context.active_object:
            mesh_map_name = mesh_map_baking.get_meshmap_name(bpy.context.active_object.name, mesh_map_type)
            if bpy.data.images.get(mesh_map_name):
                col.label(text=mesh_map_name)
            else:
                col.label(text=null_meshmap_text)
        else:
            col.label(text="No Active Object")

        col = row.column()
        col.scale_x = 0.5
        col.prop(addon_preferences.mesh_map_anti_aliasing, mesh_map_type.lower() + "_anti_aliasing", text="")

        col = row.column()
        row = col.row(align=True)
        operator = row.operator("matlayer.preview_mesh_map", text="", icon='MATERIAL_DATA')
        operator.mesh_map_type = mesh_map_type
        operator = row.operator("matlayer.delete_mesh_map", text="", icon='TRASH')
        operator.mesh_map_name = mesh_map_type

    # Draw the disable preview button.
    row = layout.row()
    row.scale_y = 1.4
    row.operator("matlayer.disable_mesh_map_preview", text="Disable Mesh Map Preview")

def draw_general_settings(layout, addon_preferences, baking_settings):
    '''Draws general settings for mesh map baking.'''
    row = layout.row()
    row.separator()
    row.scale_y = 2
    layout.label(text="GENERAL SETTINGS")

    split = layout.split(factor=0.4)
    first_column = split.column()
    second_column = split.column()

    row = first_column.row()
    row.label(text="High Poly Object")
    row = second_column.row()
    row.prop(baking_settings, "high_poly_object", text="", slider=True)

    row = first_column.row()
    row.label(text="Render Device")
    row = second_column.row()
    row.prop(bpy.data.scenes["Scene"].cycles, "device", text="")

    row = first_column.row()
    row.label(text="Mesh Map Quality")
    row = second_column.row()
    row.prop(addon_preferences, "mesh_map_quality", text="")

    row = first_column.row()
    row.label(text="Cage Mode")
    row = second_column.row()
    row.prop(addon_preferences, "cage_mode", text="")

    match addon_preferences.cage_mode:
        case 'NO_CAGE':
            row = first_column.row()
            row.label(text="Cage Extrusion")
            row = second_column.row()
            row.prop(bpy.context.scene.render.bake, "cage_extrusion", text="")

        case 'AUTO_CAGE':
            row = first_column.row()
            row.label(text="Cage Upscale")
            row = second_column.row()
            row.prop(addon_preferences, "cage_upscale", text="")

        case 'MANUAL_CAGE':
            row = first_column.row()
            row.label(text="Cage")
            row = second_column.row()
            row.prop(bpy.context.scene.render.bake, "cage_object", text="")

    row = first_column.row()
    row.label(text="Margin")
    row = second_column.row()
    row.prop(bpy.context.scene.render.bake, "margin", text="")

    row = first_column.row()
    row.label(text="Triangulate")
    row = second_column.row()
    row.prop(addon_preferences, "triangulate", text="")

    row = first_column.row()
    row.label(text="Relative to Bounding Box")
    row = second_column.row()
    row.prop(addon_preferences, "relative_to_bounding_box", text="")

def draw_curvature_settings(layout, addon_preferences):
    layout.separator()
    layout.label(text="CURVATURE")

    split = layout.split(factor=0.25)
    first_column = split.column()
    second_column = split.column()

    row = first_column.row()
    row.label(text="Edge Radius")
    row = second_column.row()
    row.prop(addon_preferences, "curvature_edge_radius", slider=True, text="")

    row = first_column.row()
    row.label(text="Edge Intensity")
    row = second_column.row()
    row.prop(addon_preferences, "curvature_edge_intensity", slider=True, text="")

    row = first_column.row()
    row.label(text="Occlusion Radius")
    row = second_column.row()
    row.prop(addon_preferences, "ambient_occlusion_intensity", slider=True, text="")

    row = first_column.row()
    row.label(text="Occlusion Samples")
    row = second_column.row()
    row.prop(addon_preferences, "ambient_occlusion_samples", slider=True, text="")

    row = layout.row()
    row.prop(addon_preferences, "ambient_occlusion_local", text="Local Occlusion")

def draw_thickness_settings(layout, addon_preferences):
    layout.separator()
    layout.label(text="THICKNESS")

    split = layout.split(factor=0.25)
    first_column = split.column()
    second_column = split.column()

    row = first_column.row()
    row.label(text="Samples")
    row = second_column.row()
    row.prop(addon_preferences, "thickness_samples", slider=True, text="")

def draw_normal_settings(layout):
    layout.separator()
    layout.label(text="NORMALS")

    split = layout.split(factor=0.25)
    first_column = split.column()
    second_column = split.column()

    row = first_column.row()
    row.label(text="Cage Extrusion")
    row = second_column.row()
    row.prop(bpy.data.scenes["Scene"].render.bake, "cage_extrusion", slider=True)

    row = first_column.row()
    row.label(text="Max Ray Distance")
    row = second_column.row()
    row.prop(bpy.data.scenes["Scene"].render.bake, "max_ray_distance", slider=True)

def draw_mesh_map_settings(layout, addon_preferences):
    '''Draws settings for individual mesh maps.'''
    layout.separator()

    layout.label(text="MESH MAP SETTINGS")

    split = layout.split(factor=0.3)
    first_column = split.column()
    second_column = split.column()
    
    row = first_column.row()
    row.label(text="Occlusion Samples")
    row = second_column.row()
    row.prop(addon_preferences, "occlusion_samples", slider=True, text="")

    row = first_column.row()
    row.label(text="Occlusion Distance")
    row = second_column.row()
    row.prop(addon_preferences, "occlusion_distance", slider=True, text="")

    row = first_column.row()
    row.label(text="Occlusion Intensity")
    row = second_column.row()
    row.prop(addon_preferences, "occlusion_intensity", slider=True, text="")

    row = first_column.row()
    row.label(text="Local Occlusion")
    row = second_column.row()
    row.prop(addon_preferences, "local_occlusion", text="")

def draw_baking_section_ui(self, context):
    '''Draws the baking section user interface'''
    ui_section_tabs.draw_section_tabs(self, context)

    layout = self.layout

    if "cycles" not in bpy.context.preferences.addons:
        layout.label(text="Cycles add-on is not enabled.")
        layout.label(text="Enable Cyles from Blender's add-ons in for baking to work.")
        layout.label(text="Edit -> Preferences -> Add-ons -> Cycles Render Engine")
        return

    baking_settings = context.scene.matlayer_baking_settings
    addon_preferences = bpy.context.preferences.addons[preferences.ADDON_NAME].preferences

    # Draw bake button.
    row = layout.row()
    row.scale_y = 2.0
    row.operator("matlayer.batch_bake", text="Bake")
    row.operator("matlayer.open_bake_folder", text="", icon='FILE_FOLDER')

    draw_mesh_map_status(layout, addon_preferences)
    draw_general_settings(layout, addon_preferences, baking_settings)
    draw_mesh_map_settings(layout, addon_preferences)