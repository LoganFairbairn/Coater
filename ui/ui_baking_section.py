# This files handles drawing baking section user interface.

import bpy
from .import ui_section_tabs

def draw_ambient_occlusion_settings(layout, baking_settings, scale_y):
    layout.label(text="Ambient Occlusion Bake Settings:")
    row = layout.row()
    row.scale_y = scale_y
    row.prop(baking_settings, "ambient_occlusion_intensity", slider=True)
    
    row = layout.row()
    row.scale_y = scale_y
    row.prop(baking_settings, "ambient_occlusion_samples", slider=True)

    row = layout.row()
    row.scale_y = scale_y
    row.prop(baking_settings, "ambient_occlusion_local")
    row.prop(baking_settings, "ambient_occlusion_inside")

def draw_curvature_settings(layout, baking_settings, scale_y):
    layout.label(text="Curvature Bake Settings:")

    row = layout.row()
    row.scale_y = scale_y
    row.prop(baking_settings, "curvature_edge_radius", slider=True)

    row = layout.row()
    row.scale_y = scale_y
    row.prop(baking_settings, "curvature_edge_intensity", slider=True)

    row = layout.row()
    row.scale_y = scale_y
    row.prop(baking_settings, "ambient_occlusion_intensity", slider=True)

    row = layout.row()
    row.scale_y = scale_y
    row.prop(baking_settings, "ambient_occlusion_samples", slider=True)

    row = layout.row()
    row.scale_y = scale_y
    row.prop(baking_settings, "ambient_occlusion_local")
    row.prop(baking_settings, "ambient_occlusion_inside")

def draw_thickness_settings(layout, baking_settings, scale_y):
    layout.label(text="Thickness Bake Settings")

def draw_normal_settings(layout, baking_settings, scale_y):
    layout.label(text="Normal Bake Settings")

def draw_baking_section_ui(self, context):
    '''Draws the baking section user interface'''
    ui_section_tabs.draw_section_tabs(self, context)

    layout = self.layout
    baking_settings = context.scene.matlay_baking_settings

    # Draw bake button.
    row = layout.row()
    row.operator("matlay.bake")
    row.scale_y = 2.0

    # Draw baking types.
    scale_y = 1.4

    row = layout.row()
    row.scale_y = scale_y
    row.prop(baking_settings, "bake_ambient_occlusion", text="")
    row.label(text="Ambient Occlusion")
    row.operator("matlay.bake_ambient_occlusion", text="", icon='RENDER_STILL')
    row.operator("matlay.delete_ao_map", icon='TRASH', text="")

    row = layout.row()
    row.scale_y = scale_y
    row.prop(baking_settings, "bake_curvature", text="")
    row.label(text="Curvature")
    row.operator("matlay.bake_curvature", text="", icon='RENDER_STILL')
    row.operator("matlay.delete_curvature_map", icon='TRASH', text="")

    row = layout.row()
    row.scale_y = scale_y
    row.prop(baking_settings, "bake_thickness", text="")
    row.label(text="Thickness")
    row.operator("matlay.bake_thickness", text="", icon='RENDER_STILL')
    row.operator("matlay.delete_thickness_map", icon='TRASH', text="")

    row = layout.row()
    row.scale_y = scale_y
    row.prop(baking_settings, "bake_normals", text="")
    row.label(text="Normal")
    row.operator("matlay.bake_normals", text="", icon='RENDER_STILL')
    row.operator("matlay.delete_normal_map", icon='TRASH', text="")

    #----------------------------- BAKE SETTINGS -----------------------------#

    split = layout.split()
    col = split.column()
    col.ui_units_x = 1
    col.scale_y = scale_y
    col.prop(baking_settings, "output_width", text="")

    col = split.column()
    col.ui_units_x = 0.1
    col.scale_y = scale_y
    if baking_settings.match_bake_resolution:
        col.prop(baking_settings, "match_bake_resolution", text="", icon="LOCKED")

    else:
        col.prop(baking_settings, "match_bake_resolution", text="", icon="UNLOCKED")

    col = split.column()
    col.ui_units_x = 2
    col.scale_y = scale_y
    if baking_settings.match_bake_resolution:
        col.enabled = False
        
    col.prop(baking_settings, "output_height", text="")

    row = layout.row()
    row.scale_y = scale_y
    row.prop(baking_settings, "high_poly_mesh", slider=True)

    row = layout.row()
    row.scale_y = scale_y
    row.prop(bpy.data.scenes["Scene"].cycles, "device", text="")

    #----------------------------- ADVANCED SETTINGS -----------------------------#

    if not baking_settings.show_advanced_settings:
        row = layout.row()
        row.scale_x = 10000
        row.prop(baking_settings, "show_advanced_settings", icon='TRIA_DOWN', text="")

    if baking_settings.show_advanced_settings:
        layout.label(text="ADVANCED SETTINGS")

        row = layout.row()
        row.scale_y = scale_y
        row.prop(baking_settings, "output_quality", text="")

        row = layout.row()
        row.scale_y = scale_y
        row.prop(bpy.data.scenes["Scene"].render.bake, "margin", slider=True)

        row = layout.row()
        row.scale_y = scale_y
        row.prop(baking_settings, "bake_type", text="")

        match baking_settings.bake_type:
            case 'AMBIENT_OCCLUSION':
                draw_ambient_occlusion_settings(layout, baking_settings, scale_y)

            case 'CURVATURE':
                draw_curvature_settings(layout, baking_settings, scale_y)

            case 'THICKNESS':
                draw_thickness_settings(layout, baking_settings, scale_y)

            case 'NORMAL':
                draw_normal_settings(layout, baking_settings, scale_y)

        row = layout.row()
        row.scale_x = 10000
        row.prop(baking_settings, "show_advanced_settings", icon='TRIA_UP', text="")