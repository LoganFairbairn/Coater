import bpy
from bpy.types import Operator
from bpy_extras.io_utils import ImportHelper        # For importing images.
from ..core import debug_logging                    # For printing / displaying debugging related messages.
from ..core import image_utilities                  # For access to image related helper functions.
from ..core import material_layers                  # For accessing material layer nodes.
from ..core import layer_masks                      # For editing layer masks.
from ..core import blender_addon_utils              # For extra helpful Blender utilities.
import os                                           # For saving layer images.
import re                                           # For splitting strings to identify material channels.

# Dictionary of words / tags that may be in image texture names that could be used to identify material channels from image file names.
MATERIAL_CHANNEL_TAGS = {
    "color": 'COLOR',
    "colour": 'COLOR',
    "couleur": 'COLOR',
    "diffuse": 'COLOR',
    "diff": 'COLOR',
    "dif": 'COLOR',
    "subsurface": 'SUBSURFACE',
    "subsurf": 'SUBSURFACE',
    "ss": 'SUBSURFACE',
    "metallic": 'METALLIC',
    "metalness": 'METALLIC',
    "metal": 'METALLIC',
    "métalique": 'METALLIC',
    "metalique": 'METALLIC',
    "specular": 'SPECULAR',
    "specularité": 'SPECULAR',
    "specularite": 'SPECULAR',
    "spec": 'SPECULAR',
    "roughness": 'ROUGHNESS',
    "rough": 'ROUGHNESS',
    "rugosité": 'ROUGHNESS',
    "rugosite": 'ROUGHNESS',
    "emission": 'EMISSION',
    "émission": 'EMISSION',
    "emit": 'EMISSION',
    "normal": 'NORMAL',
    "normale": 'NORMAL',
    "nor": 'NORMAL',
    "ngl": 'NORMAL',
    "ndx": 'NORMAL',
    "height": 'HEIGHT',
    "hauteur": 'HEIGHT',
    "bump": 'HEIGHT',
    "opacity": 'ALPHA',
    "opaque": 'ALPHA',
    "alpha": 'ALPHA',

    # RGB channel packing...
    "ORM": 'CHANNEL_PACKED',
    "RMO": 'CHANNEL_PACKED',

    # RGBA channel packing, 'X' is used to identify when nothing is packed into a channel.
    "MOXS": 'CHANNEL_PACKED',
}

# https://docs.unrealengine.com/4.27/en-US/ProductionPipelines/AssetNaming/
# With an identifiable material channel format, such as the one used commonly in game engines (T_MyTexture_C_1),
# we can identify material channels using only the first few letters.
MATERIAL_CHANNEL_SHORTHAND = {
    "C": 'COLOR',
    "M": 'METALLIC',
    "R": 'ROUGHNESS',
    "N": 'NORMAL',
    "NGL": 'NORMAL',
    "NDX": 'NORMAL',
    "H": 'HEIGHT',
    "B": 'HEIGHT',
    "S": 'SPECULAR',
    "SS": 'SUBSURFACE',
    "A": 'ALPHA',
    "CC": 'COAT',
    "E": 'EMISSION'
    #"O": "OCCLUSION",
}

class MATLAYER_OT_import_texture_set(Operator, ImportHelper):
    bl_idname = "matlayer.import_texture_set"
    bl_label = "Import Texture Set"
    bl_description = "Imports multiple selected textures into material channels based on file names. This function requires decent texture file naming conventions to work properly"
    bl_options = {'REGISTER', 'UNDO'}

    files: bpy.props.CollectionProperty(
        type=bpy.types.OperatorFileListElement,
        options={'HIDDEN', 'SKIP_SAVE'}
    )

    filter_glob: bpy.props.StringProperty(
        default='*.jpg;*.jpeg;*.png;*.tif;*.tiff;*.bmp;*.exr',
        options={'HIDDEN'}
    )

    def execute(self, context):
        # Helper function to split the file name into components.
        def split_filename_by_components(filename):
            # Remove file extension.
            filename = os.path.splitext(filename)[0]

            # Remove numbers (these can't be used to identify a material channel from the texture name).
            filename = ''.join(i for i in filename if not i.isdigit())
            
            # Separate camel case by space.
            filename = re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', filename))

            # Replace common separators with a space.
            separators = ['_', '.', '-', '__', '--', '#']
            for seperator in separators:
                filename = filename.replace(seperator, ' ')

            # Return all components split by a space with lowercase characters.
            split_components = filename.split(' ')
            components = []
            for c in split_components:
                if c != '':
                    components.append(c.lower())

            return components

        # Compile a list of all unique tags found accross all user selected image file names.
        material_channel_occurance = {}
        for file in self.files:
            tags = split_filename_by_components(file.name)
            for tag in tags:
                if tag not in material_channel_occurance and tag in MATERIAL_CHANNEL_TAGS:
                    material_channel = MATERIAL_CHANNEL_TAGS[tag]
                    material_channel_occurance[material_channel] = 0

        # Calculate how many times a unique channel tag appears accross all user selected image files.
        for file in self.files:
            tags = split_filename_by_components(file.name)
            for tag in tags:
                if tag in MATERIAL_CHANNEL_TAGS:
                    material_channel = MATERIAL_CHANNEL_TAGS[tag]
                    if material_channel in material_channel_occurance:
                        material_channel_occurance[material_channel] += 1

        # Cycle through all selected image files and try to identify the correct material channel to import them into.
        selected_image_file = False
        for file in self.files:
            detected_material_channel = 'NONE'
            
            # If the image file starts with a 'T_' assume it's using a commonly used Unreal Engine / game engine naming convention.
            if file.name.startswith('T_'):
                remove_file_extension = file.name.split('.')[0]
                short_material_channel = remove_file_extension.split('_')[2]
                if short_material_channel in MATERIAL_CHANNEL_SHORTHAND:
                    detected_material_channel = MATERIAL_CHANNEL_SHORTHAND[short_material_channel]

            # For image files that don't start with 'T_' guess the material channel by parsing for tags in the file name that would ID it.
            else:

                # Create a list of tags used in this files name.
                tags = split_filename_by_components(file.name)
                channel_tags_in_filename = []
                for tag in tags:
                    if tag in MATERIAL_CHANNEL_TAGS:
                        channel_tags_in_filename.append(MATERIAL_CHANNEL_TAGS[tag])

                # Don't import files that have no material channel tag detected in it's file name.
                if len(channel_tags_in_filename) > 0:

                    # Start by assuming the correct material channel is the one that appears the least in the file name.
                    # I.E: Selected files: RoughMetal_002_2k_Color, RoughMetal_002_2k_Normal, RoughMetal_002_2k_Metallic, RoughMetal_002_2k_Rough
                    # For the first file in the above example, the correct material channel would be color,
                    # because 'metallic' appears more than once accross all user selected image files.
                    detected_material_channel = channel_tags_in_filename[0]
                    material_channel_occurances_equal = True
                    for material_channel_name in channel_tags_in_filename:
                        if material_channel_occurance[material_channel_name] < material_channel_occurance[detected_material_channel]:
                            detected_material_channel = material_channel_name
                            material_channel_occurances_equal = False
                    
                    # If all material channels identified in the files name occur equally throughout all selected filenames,
                    # use the material channel that occurs the most in the files name.
                    # I.E: Selected files: RoughMetal_002_2k_Color, RoughMetal_002_2k_Normal, RoughMetal_002_2k_Metallic, RoughMetal_002_2k_Rough
                    # For the third file in the above example, the correct material channel is 'metallic' because that tag appears twice in the name.
                    if material_channel_occurances_equal:
                        for material_channel_name in channel_tags_in_filename:
                            if material_channel_occurance[material_channel_name] > material_channel_occurance[detected_material_channel]:
                                detected_material_channel = material_channel_name

            # TODO: If the image is detected to be using channel packing, create a list of channels to place the texture into.
            
            # TODO: Change all material channels to use texture nodes (if they aren't using one already).
            selected_layer_index = bpy.context.scene.matlayer_layer_stack.selected_layer_index
            value_node = material_layers.get_material_layer_node('VALUE', selected_layer_index, detected_material_channel)
            if value_node.bl_static_type != 'TEX_IMAGE':
                material_layers.replace_material_channel_node(detected_material_channel, 'TEXTURE')

            # TODO: If the image is detected to be using channel packing, adjust the output of the material channel.
            

            # Import the image only if the material channel was detected.
            if detected_material_channel != 'NONE':
                folder_directory = os.path.split(self.filepath)
                image_path = os.path.join(folder_directory[0], file.name)
                bpy.ops.image.open(filepath=image_path)
                imported_image = bpy.data.images[file.name]

                # Select the first image file in the canvas painting window.
                if selected_image_file == False:
                    context.scene.tool_settings.image_paint.canvas = imported_image
                    selected_image_file = True

                # Place the image into a material nodes based on texture projection and inferred material channel name.
                projection_node = material_layers.get_material_layer_node('PROJECTION', selected_layer_index)
                match projection_node.node_tree.name:
                    case 'ML_UVProjection':
                        value_node = material_layers.get_material_layer_node('VALUE', selected_layer_index, detected_material_channel)
                        if value_node.bl_static_type == 'TEX_IMAGE':
                            value_node.image = imported_image

                    case 'ML_TriplanarProjection':
                        for i in range(0, 3):
                            value_node = material_layers.get_material_layer_node('VALUE', selected_layer_index, detected_material_channel, node_number=i + 1)
                            if value_node.bl_static_type == 'TEX_IMAGE':
                                value_node.image = imported_image

                # Update the imported images colorspace based on it's specified material channel.
                image_utilities.set_image_colorspace_by_material_channel(imported_image, detected_material_channel)

                # TODO: Only check for DirectX normal maps if selected material channel is normal.
                # Print information about using DirectX normal maps for users if it's detected they are using one.
                if image_utilities.check_for_directx(file.name):
                    self.report({'INFO'}, "DirectX normal map import detected, normals may be inverted. You should use an OpenGL normal map instead.")

                # Copy the imported image to a folder next to the blend file for file management purposes.
                # This happens only if 'save imported textures' is on in the add-on preferences.
                image_utilities.save_raw_image(image_path, imported_image.name)

            else :
                debug_logging.log("No material channel detected for file: {0}".format(file.name))

        return {'FINISHED'}
    
class MATLAYER_OT_merge_materials(Operator):
    bl_idname = "matlayer.merge_materials"
    bl_label = "Merge Materials"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Merges all layers from the selected material into the active material. Any mesh map textures in the merged material will be replaced by the mesh maps on the active object"

    def execute(self, context):
        if blender_addon_utils.verify_material_operation_context(self) == False:
            return {'FINISHED'}

        merge_material = bpy.context.scene.matlayer_merge_material
        if merge_material:
            layer_count = material_layers.count_layers(merge_material)
            if (layer_count) <= 0:
                debug_logging.log_status("No layers to merge in the merge material.", self, type='ERROR')
                return {'FINISHED'}

            else:
                active_material = bpy.context.active_object.active_material
                for i in range(0, layer_count):
                    
                    # Duplicate the layer node tree and add a new layer group node to the tree.
                    merge_layer_node = merge_material.node_tree.nodes.get(str(i))
                    if merge_layer_node:
                        if merge_layer_node.node_tree:
                            duplicated_node_tree = blender_addon_utils.duplicate_node_group(merge_layer_node.node_tree.name)
                            if duplicated_node_tree:
                                new_layer_slot_index = material_layers.add_material_layer_slot()

                                duplicated_node_tree.name = "{0}_{1}".format(active_material.name, str(new_layer_slot_index))
                                new_layer_group_node = active_material.node_tree.nodes.new('ShaderNodeGroup')
                                new_layer_group_node.node_tree = duplicated_node_tree
                                new_layer_group_node.name = str(new_layer_slot_index) + "~"
                                new_layer_group_node.label = merge_layer_node.label
                                
                                material_layers.reindex_layer_nodes(change_made='ADDED_LAYER', affected_layer_index=new_layer_slot_index)
                                material_layers.organize_layer_group_nodes()
                                material_layers.link_layer_group_nodes(self)
                                layer_masks.organize_mask_nodes()

                        # Clear the mask stack from the new layer.
                        masks = bpy.context.scene.matlayer_masks
                        masks.clear()

                        # Duplicate all masks associated with that layer.
                        mask_count = layer_masks.count_masks(i)
                        for c in range(0, mask_count):
                            original_mask_node = layer_masks.get_mask_node('MASK', i, c)
                            if original_mask_node:
                                duplicated_node_tree = blender_addon_utils.duplicate_node_group(original_mask_node.node_tree.name)
                                if duplicated_node_tree:
                                    new_mask_slot_index = layer_masks.add_mask_slot()
                                    duplicated_mask_name = layer_masks.format_mask_name(bpy.context.active_object.active_material.name, new_layer_slot_index, new_mask_slot_index) + "~"
                                    duplicated_node_tree.name = duplicated_mask_name
                                    new_mask_group_node = active_material.node_tree.nodes.new('ShaderNodeGroup')
                                    new_mask_group_node.node_tree = duplicated_node_tree
                                    new_mask_group_node.name = duplicated_mask_name
                                    new_mask_group_node.label = original_mask_node.label

                                    layer_masks.reindex_masks('ADDED_MASK', new_layer_slot_index, affected_mask_index=i)

                        layer_masks.link_mask_nodes(new_layer_slot_index)
                        layer_masks.organize_mask_nodes()

            bpy.context.scene.matlayer_merge_material = None
            debug_logging.log_status("Merged materials.", self, type='INFO')

        else:
            debug_logging.log_status("Merge material specified is empty, or invalid.", self, type='ERROR')
            return {'FINISHED'}
        return {'FINISHED'}