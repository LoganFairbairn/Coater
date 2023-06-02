# Copyright (c) 2021-2023 Logan Fairbairn
# logan-fairbairn@outlook.com
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

# This file imports and registers all required modules for this add-on.

import bpy
from bpy.props import PointerProperty, CollectionProperty
import bpy.utils.previews       # Imported for loading texture previews as icons.
from bpy.app.handlers import persistent

# Import add-on preference settings.
from .preferences import AddonPreferences

# Import texture set modules.
from .core.texture_set_settings import MATLAYER_texture_set_settings, GlobalMaterialChannelToggles

# Import layer related modules.
from .core.material_layers import *

# Import material channel modules.
from .core.material_channels import MATLAYER_OT_toggle_material_channel_preview

# Import layer masking modules.
from .core.layer_masks import MaskProjectionSettings, MATLAYER_mask_stack, MATLAYER_masks, MATLAYER_UL_mask_stack, MATLAYER_OT_add_black_layer_mask, MATLAYER_OT_add_white_layer_mask, MATLAYER_OT_add_empty_layer_mask, MATLAYER_OT_add_group_node_layer_mask, MATLAYER_OT_add_noise_layer_mask, MATLAYER_OT_add_voronoi_layer_mask, MATLAYER_OT_add_musgrave_layer_mask, MATLAYER_OT_open_layer_mask_menu, MATLAYER_OT_delete_layer_mask,MATLAYER_OT_move_layer_mask_up, MATLAYER_OT_move_layer_mask_down, MATLAYER_OT_add_mask_image, MATLAYER_OT_delete_mask_image, MATLAYER_OT_import_mask_image, MATLAYER_mask_filter_stack, MATLAYER_mask_filters, MATLAYER_UL_mask_filter_stack, MATLAYER_OT_add_mask_filter_invert, MATLAYER_OT_add_mask_filter_val_to_rgb, MATLAYER_OT_add_layer_mask_filter_menu, MATLAYER_OT_delete_mask_filter, MATLAYER_OT_move_layer_mask_filter

# Import layer operations.
from .core.layer_operations import *

# Import material filter modules.
from .core.material_filters import FiltersMaterialChannelToggles, MATLAYER_material_filter_stack, MATLAYER_UL_layer_filter_stack, MATLAYER_material_filters, MATLAYER_OT_add_layer_filter_menu, MATLAYER_OT_add_layer_filter_rgb_curves, MATLAYER_OT_add_layer_filter_hsv, MATLAYER_OT_add_layer_filter_invert, MATLAYER_OT_add_layer_filter_val_to_rgb, MATLAYER_OT_add_layer_filter_bright_contrast, MATLAYER_OT_add_material_filter_normal_intensity, MATLAYER_OT_delete_layer_filter, MATLAYER_OT_move_layer_filter_up, MATLAYER_OT_move_layer_filter_down

# Import baking modules.
from .core.baking import MATLAYER_baking_settings, MATLAYER_OT_bake, MATLAYER_OT_bake_ambient_occlusion, MATLAYER_OT_bake_curvature, MATLAYER_OT_bake_thickness, MATLAYER_OT_bake_normals, MATLAYER_OT_delete_ao_map, MATLAYER_OT_delete_curvature_map, MATLAYER_OT_delete_thickness_map, MATLAYER_OT_delete_normal_map

# Import exporting modules.
from .core.exporting import MATLAYER_exporting_settings, MATLAYER_OT_export, MATLAYER_OT_export_base_color, MATLAYER_OT_export_subsurface, MATLAYER_OT_export_subsurface_color, MATLAYER_OT_export_metallic, MATLAYER_OT_export_specular, MATLAYER_OT_export_roughness, MATLAYER_OT_export_normals, MATLAYER_OT_export_height, MATLAYER_OT_export_emission

# Import tool / utility modules.
from .utilities.image_file_handling import MATLAYER_OT_add_layer_image, MATLAYER_OT_delete_layer_image, MATLAYER_OT_import_texture, MATLAYER_OT_import_texture_set

# Import settings.
from .utilities.internal_utils import MatlayerSettings, MATLAYER_OT_set_decal_layer_snapping, MATLAYER_OT_append_workspace, MATLAYER_OT_append_basic_brushes, MATLAYER_OT_delete_unused_external_images

# Import user interface modules.
from .ui.main_ui import *
from .ui.popup_add_mask import *
from .ui.ui_layer_stack import *

bl_info = {
    "name": "MatLayer",
    "author": "Logan Fairbairn (Ryver)",
    "version": (1, 0, 5),
    "blender": (3, 5, 0),
    "location": "View3D > Sidebar > MatLayer",
    "description": "Replaces node based texturing workflow with a layer stack workflow through a custom user interface.",
    "warning": "",
    "doc_url": "",
    "category": "Material Editing",
}

# List of classes to be registered.
classes = (
    # Preferences
    AddonPreferences,

    # Baking
    MATLAYER_baking_settings,
    MATLAYER_OT_bake,
    MATLAYER_OT_bake_ambient_occlusion,
    MATLAYER_OT_bake_curvature,
    MATLAYER_OT_bake_thickness,
    MATLAYER_OT_bake_normals,
    MATLAYER_OT_delete_ao_map,
    MATLAYER_OT_delete_curvature_map,
    MATLAYER_OT_delete_thickness_map,
    MATLAYER_OT_delete_normal_map,

    # Exporting
    MATLAYER_exporting_settings,
    MATLAYER_OT_export,
    MATLAYER_OT_export_base_color,
    MATLAYER_OT_export_subsurface,
    MATLAYER_OT_export_subsurface_color,
    MATLAYER_OT_export_metallic,
    MATLAYER_OT_export_specular,
    MATLAYER_OT_export_roughness,
    MATLAYER_OT_export_normals,
    MATLAYER_OT_export_height,
    MATLAYER_OT_export_emission,

    # Material Channels
    MATLAYER_OT_toggle_material_channel_preview,

    # Layers
    MaterialChannelToggles,
    MaterialChannelNodeType,
    ProjectionSettings,
    MaterialChannelTextures,
    MaterialChannelColors,
    MaterialChannelUniformValues,
    MaterialChannelGroupNodes,
    MaterialChannelBlurring,
    MATLAYER_OT_open_material_layer_settings,
    MATLAYER_layer_stack,
    MATLAYER_layers,

    # Masks
    MaskProjectionSettings,
    MATLAYER_mask_stack,
    MATLAYER_masks,
    MATLAYER_UL_mask_stack,
    MATLAYER_OT_add_black_layer_mask, 
    MATLAYER_OT_add_white_layer_mask,
    MATLAYER_OT_add_empty_layer_mask,
    MATLAYER_OT_add_group_node_layer_mask,
    MATLAYER_OT_add_noise_layer_mask,
    MATLAYER_OT_add_voronoi_layer_mask,
    MATLAYER_OT_add_musgrave_layer_mask,
    MATLAYER_OT_open_layer_mask_menu,
    MATLAYER_OT_delete_layer_mask,
    MATLAYER_OT_move_layer_mask_up,
    MATLAYER_OT_move_layer_mask_down,
    MATLAYER_OT_add_mask_image, 
    MATLAYER_OT_delete_mask_image, 
    MATLAYER_OT_import_mask_image,

    # Mask Filters
    MATLAYER_mask_filter_stack,
    MATLAYER_mask_filters,
    MATLAYER_UL_mask_filter_stack,
    MATLAYER_OT_add_mask_filter_invert,
    MATLAYER_OT_add_mask_filter_val_to_rgb,
    MATLAYER_OT_add_layer_mask_filter_menu,
    MATLAYER_OT_delete_mask_filter,
    MATLAYER_OT_move_layer_mask_filter,

    # Filters
    FiltersMaterialChannelToggles,
    MATLAYER_material_filter_stack, 
    MATLAYER_UL_layer_filter_stack,
    MATLAYER_material_filters,
    MATLAYER_OT_add_layer_filter_rgb_curves,
    MATLAYER_OT_add_layer_filter_hsv,
    MATLAYER_OT_add_layer_filter_invert,
    MATLAYER_OT_add_layer_filter_val_to_rgb,
    MATLAYER_OT_add_layer_filter_bright_contrast,
    MATLAYER_OT_add_material_filter_normal_intensity,
    MATLAYER_OT_delete_layer_filter,
    MATLAYER_OT_move_layer_filter_up,
    MATLAYER_OT_move_layer_filter_down,
    MATLAYER_OT_add_mask_menu,
    MATLAYER_OT_add_layer_filter_menu,

    # Layer Operations
    MATLAYER_UL_layer_list,
    MATLAYER_OT_add_decal_layer,
    MATLAYER_OT_add_material_layer,
    MATLAYER_OT_add_paint_layer,
    MATLAYER_OT_add_layer_menu,
    MATLAYER_OT_delete_layer,
    MATLAYER_OT_duplicate_layer,
    MATLAYER_OT_move_material_layer,
    MATLAYER_OT_import_texture,
    MATLAYER_OT_import_texture_set,
    MATLAYER_OT_read_layer_nodes,
    MATLAYER_OT_add_layer_image,
    MATLAYER_OT_delete_layer_image,
    MATLAYER_OT_edit_uvs_externally,
    MATLAYER_OT_edit_image_externally,
    MATLAYER_OT_reload_image,

    # Texture Set Settings
    GlobalMaterialChannelToggles,
    MATLAYER_texture_set_settings,

    # Utilities
    MatlayerSettings,
    MATLAYER_OT_set_decal_layer_snapping,
    MATLAYER_OT_append_workspace,
    MATLAYER_OT_append_basic_brushes,
    MATLAYER_OT_delete_unused_external_images,

    # Main Panel
    MATLAYER_panel_properties,
    MATLAYER_PT_Panel
)

# Read material nodes when the active material index is updated.
def on_active_material_index_changed():
    bpy.context.scene.matlayer_layer_stack.layer_index = 0
    bpy.ops.matlayer.read_layer_nodes(auto_called=True)

# Read material nodes for the active material when a different object is selected.
def on_active_object_changed():
    '''Triggers a layer stack refresh when the selected object changes.'''
    bpy.ops.matlayer.read_layer_nodes(auto_called=True)
    bpy.msgbus.clear_by_owner(bpy.types.Scene.active_material_index_owner)
    active = bpy.context.view_layer.objects.active
    if active:
        bpy.msgbus.subscribe_rna(
            key=active.path_resolve("active_material_index", False),
            owner=bpy.types.Scene.active_material_index_owner,
            notify=on_active_material_index_changed,
            args=()
        )

# Mark load handlers as persistent so they are not freed when loading a new blend file.
@persistent
def load_handler(dummy):
    subscribe_to = bpy.types.LayerObjects, "active"
    bpy.types.Scene.matlayer_object_selection_updater = object()
    bpy.msgbus.subscribe_rna(key=subscribe_to, owner=bpy.types.Scene.matlayer_object_selection_updater, args=(), notify=on_active_object_changed)

    # Active Material Index
    bpy.types.Scene.active_material_index_owner = object()
    bpy.msgbus.clear_by_owner(bpy.types.Scene.active_material_index_owner)
    active = bpy.context.view_layer.objects.active
    if active:
        bpy.msgbus.subscribe_rna(
            key=active.path_resolve("active_material_index", False),
            owner=bpy.types.Scene.active_material_index_owner,
            notify=on_active_material_index_changed,
            args=()
        )

    # Read active material settings when the blender file loads.
    active_object = bpy.context.active_object
    if active_object:
        if active_object.active_material:
            bpy.ops.matlayer.read_layer_nodes(auto_called=True)

# Run function on loading a new blend file.
bpy.app.handlers.load_post.append(load_handler)

def register():
    # Register properties, operators and pannels.
    for cls in classes:
        bpy.utils.register_class(cls)
        
    # Settings
    bpy.types.Scene.matlayer_settings = PointerProperty(type=MatlayerSettings)

    # Panel Properties
    bpy.types.Scene.matlayer_panel_properties = PointerProperty(type=MATLAYER_panel_properties)

    # Layer Properties
    bpy.types.Scene.matlayer_layer_stack = PointerProperty(type=MATLAYER_layer_stack)
    bpy.types.Scene.matlayer_layers = CollectionProperty(type=MATLAYER_layers)

    # Material Filter Properties
    bpy.types.Scene.matlayer_material_filter_stack = PointerProperty(type=MATLAYER_material_filter_stack)
    bpy.types.Scene.matlayer_material_filters = CollectionProperty(type=MATLAYER_material_filters)

    # Layer Mask Properites
    bpy.types.Scene.matlayer_mask_stack = PointerProperty(type=MATLAYER_mask_stack)
    bpy.types.Scene.matlayer_masks = CollectionProperty(type=MATLAYER_masks)
    bpy.types.Scene.matlayer_mask_filter_stack = PointerProperty(type=MATLAYER_mask_filter_stack)
    bpy.types.Scene.matlayer_mask_filters = CollectionProperty(type=MATLAYER_mask_filters)

    # Settings
    bpy.types.Scene.matlayer_texture_set_settings = PointerProperty(type=MATLAYER_texture_set_settings)
    bpy.types.Scene.matlayer_baking_settings = PointerProperty(type=MATLAYER_baking_settings)
    bpy.types.Scene.matlayer_export_settings = PointerProperty(type=MATLAYER_exporting_settings)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
