import bpy
from bpy.types import Operator

from ..import layer_nodes
from ..import material_channels
from ..import update_layer_nodes
from ..import add_layer_slot
from ..import coater_material_functions
from ..import set_material_shading

class COATER_OT_add_layer(Operator):
    '''Adds a layer with default numeric material values to the layer stack'''
    bl_idname = "coater.add_layer"
    bl_label = "Add Layer"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Adds a layer with default numeric material values to the layer stack"

    def execute(self, context):
        coater_material_functions.ready_coater_material(context)
        material_channels.create_channel_group_nodes(context)
        add_layer_slot.add_layer_slot(context)
        create_default_layer_nodes(context)
        update_layer_nodes.organize_all_nodes(context)
        #update_layer_nodes.link_layers(context)
        set_material_shading.set_material_shading(context)
        return {'FINISHED'}

def create_default_layer_nodes(context):
    '''Creates default nodes in all material channels for a layer.'''
    add_default_color_channel_nodes(context)
    #add_default_metallic_channel_nodes(context)
    #add_default_roughness_channel_nodes(context)
    #add_default_normal_channel_nodes(context)
    #add_default_height_channel_nodes(context)
    #add_default_scattering_channel_nodes(context)
    #add_default_emission_channel_nodes(context)




def add_default_color_channel_nodes(context):
    material_channel_node = material_channels.get_material_channel_node(context, "COLOR")

    if verify_material_channel(material_channel_node) == False:
        return

    # Add nodes that will be in all layers.
    layers = context.scene.coater_layers
    selected_layer_index = context.scene.coater_layer_stack.layer_index
    general_nodes = add_general_layer_nodes(material_channel_node, layers, selected_layer_index)

    # Create and setup nodes specific to this material channel.
    texture_node = material_channel_node.node_tree.nodes.new(type='ShaderNodeRGB')
    texture_node.name = "TEXTURE_"
    texture_node.label = texture_node.name
    layers[selected_layer_index].texture_node_name = texture_node.name
    texture_node.outputs[0].default_value = (0.25, 0.25, 0.25, 1.0)

    # Link newly created nodes.
    link_new_default_nodes(material_channel_node, texture_node, general_nodes)

    # Frame new nodes.
    frame_new_default_nodes(material_channel_node, layers, selected_layer_index)
    
    # Update node layer indicies.
    update_layer_nodes.update_layer_node_indicies(context, "COLOR")

    # TODO: Mute layer nodes based on texture set settings.
    #texture_set_settings = context.scene.coater_texture_set_settings
    #if texture_set_settings.color_channel_toggle == False:


def add_default_metallic_channel_nodes(context):
    material_channel_node = material_channels.get_material_channel_node(context, "METALLIC")

    if verify_material_channel(material_channel_node) == False:
        return

    # Add nodes that will be in all layers.
    layers = context.scene.coater_layers
    selected_layer_index = context.scene.coater_layer_stack.layer_index
    general_nodes = add_general_layer_nodes(material_channel_node, layers, selected_layer_index)

    # Create and setup nodes specific to this material channel.
    texture_node = material_channel_node.node_tree.nodes.new(type='ShaderNodeClamp')
    texture_node.name = "TEXTURE_"
    texture_node.label = texture_node.name
    layers[selected_layer_index].texture_node_name = texture_node.name
    texture_node.inputs[0].default_value = 0.0
    texture_node.inputs[1].default_value = 0.0
    texture_node.inputs[2].default_value = 1.0

    # Link newly created nodes.
    link_new_default_nodes(material_channel_node, texture_node, general_nodes)

    # Frame new nodes.
    frame_new_default_nodes(material_channel_node, layers, selected_layer_index)
    
    # Update node layer indicies.
    update_layer_nodes.update_layer_node_indicies(context, "METALLIC")

    # Set the texture node type.
    layers[selected_layer_index].metallic_texture_node_type = 'VALUE'

def add_default_roughness_channel_nodes(context):
    material_channel_node = material_channels.get_material_channel_node(context, "ROUGHNESS")

    if verify_material_channel(material_channel_node) == False:
        return

    # Add nodes that will be in all layers.
    layers = context.scene.coater_layers
    selected_layer_index = context.scene.coater_layer_stack.layer_index
    general_nodes = add_general_layer_nodes(material_channel_node, layers, selected_layer_index)

    # Create and setup nodes specific to this material channel.
    texture_node = material_channel_node.node_tree.nodes.new(type='ShaderNodeClamp')
    texture_node.name = "TEXTURE_"
    texture_node.label = texture_node.name
    layers[selected_layer_index].texture_node_name = texture_node.name
    texture_node.inputs[0].default_value = 0.0
    texture_node.inputs[1].default_value = 0.0
    texture_node.inputs[2].default_value = 1.0

    # Set the texture node type.
    layers[selected_layer_index].roughness_texture_node_type = 'VALUE'

    # Link newly created nodes.
    link_new_default_nodes(material_channel_node, texture_node, general_nodes)

    # Frame new nodes.
    frame_new_default_nodes(material_channel_node, layers, selected_layer_index)
    
    # Update node layer indicies.
    update_layer_nodes.update_layer_node_indicies(context, "ROUGHNESS")

def add_default_normal_channel_nodes(context):
    material_channel_node = material_channels.get_material_channel_node(context, "NORMAL")

    if verify_material_channel(material_channel_node) == False:
        return

    # Add nodes that will be in all layers.
    layers = context.scene.coater_layers
    selected_layer_index = context.scene.coater_layer_stack.layer_index
    general_nodes = add_general_layer_nodes(material_channel_node, layers, selected_layer_index)

    # Create and setup nodes specific to this material channel.
    texture_node = material_channel_node.node_tree.nodes.new(type='ShaderNodeRGB')
    texture_node.name = "TEXTURE_"
    texture_node.label = texture_node.name
    layers[selected_layer_index].texture_node_name = texture_node.name
    texture_node.outputs[0].default_value = (0.0, 0.0, 1.0, 1.0)

    # Link newly created nodes.
    link_new_default_nodes(material_channel_node, texture_node, general_nodes)

    # Frame new nodes.
    frame_new_default_nodes(material_channel_node, layers, selected_layer_index)
    
    # Update node layer indicies.
    update_layer_nodes.update_layer_node_indicies(context, "NORMAL")

def add_default_height_channel_nodes(context):
    material_channel_node = material_channels.get_material_channel_node(context, "HEIGHT")

    if verify_material_channel(material_channel_node) == False:
        return

    # Add nodes that will be in all layers.
    layers = context.scene.coater_layers
    selected_layer_index = context.scene.coater_layer_stack.layer_index
    general_nodes = add_general_layer_nodes(material_channel_node, layers, selected_layer_index)

    # Create and setup nodes specific to this material channel.
    texture_node = material_channel_node.node_tree.nodes.new(type='ShaderNodeClamp')
    texture_node.name = "TEXTURE_"
    texture_node.label = texture_node.name
    layers[selected_layer_index].texture_node_name = texture_node.name
    texture_node.inputs[0].default_value = 0.0
    texture_node.inputs[1].default_value = -1.0
    texture_node.inputs[2].default_value = 1.0

    # Set the texture node type.
    layers[selected_layer_index].height_texture_node_type = 'VALUE'

    # Link newly created nodes.
    link_new_default_nodes(material_channel_node, texture_node, general_nodes)

    # Frame new nodes.
    frame_new_default_nodes(material_channel_node, layers, selected_layer_index)
    
    # Update node layer indicies.
    update_layer_nodes.update_layer_node_indicies(context, "HEIGHT")

def add_default_scattering_channel_nodes(context):
    material_channel_node = material_channels.get_material_channel_node(context, "SCATTERING")

    if verify_material_channel(material_channel_node) == False:
        return

    # Add nodes that will be in all layers.
    layers = context.scene.coater_layers
    selected_layer_index = context.scene.coater_layer_stack.layer_index
    general_nodes = add_general_layer_nodes(material_channel_node, layers, selected_layer_index)

    # Create and setup nodes specific to this material channel.
    texture_node = material_channel_node.node_tree.nodes.new(type='ShaderNodeRGB')
    texture_node.name = "TEXTURE_"
    texture_node.label = texture_node.name
    layers[selected_layer_index].texture_node_name = texture_node.name
    texture_node.outputs[0].default_value = (1.0, 0.0, 0.0, 1.0)

    # Link newly created nodes.
    link_new_default_nodes(material_channel_node, texture_node, general_nodes)

    # Frame new nodes.
    frame_new_default_nodes(material_channel_node, layers, selected_layer_index)
    
    # Update node layer indicies.
    update_layer_nodes.update_layer_node_indicies(context, "SCATTERING")

def add_default_emission_channel_nodes(context):
    material_channel_node = material_channels.get_material_channel_node(context, "EMISSION")

    if verify_material_channel(material_channel_node) == False:
        return

    # Add nodes that will be in all layers.
    layers = context.scene.coater_layers
    selected_layer_index = context.scene.coater_layer_stack.layer_index
    general_nodes = add_general_layer_nodes(material_channel_node, layers, selected_layer_index)

    # Create and setup nodes specific to this material channel.
    texture_node = material_channel_node.node_tree.nodes.new(type='ShaderNodeRGB')
    texture_node.name = "TEXTURE_"
    texture_node.label = texture_node.name
    layers[selected_layer_index].texture_node_name = texture_node.name
    texture_node.outputs[0].default_value = (0.25, 0.25, 0.25, 1.0)

    # Link newly created nodes.
    link_new_default_nodes(material_channel_node, texture_node, general_nodes)

    # Frame new nodes.
    frame_new_default_nodes(material_channel_node, layers, selected_layer_index)
    
    # Update node layer indicies.
    update_layer_nodes.update_layer_node_indicies(context, "EMISSION")



def verify_material_channel(material_channel_node):
    if material_channel_node == None:
        print("Error, no material channel found.")
        return False
    return True

def add_default_color_channel_nodes(context):
    layers = context.scene.coater_layers
    selected_layer_index = context.scene.coater_layer_stack.layer_index
    color_material_channel_node = material_channels.get_material_channel_node(context, "COLOR")

    if color_material_channel_node == None:
        print("Error, no material channel found.")
        return

    # Add nodes that will be in all layers.
    general_nodes = add_general_layer_nodes(color_material_channel_node, layers, selected_layer_index)

    # Add nodes specific to this color channel.
    texture_node = color_material_channel_node.node_tree.nodes.new(type='ShaderNodeRGB')
    texture_node.name = "TEXTURE_"
    texture_node.label = texture_node.name

    # Store the new node names in the layer.
    layers[selected_layer_index].texture_node_name = texture_node.name
    texture_node.outputs[0].default_value = (0.25, 0.25, 0.25, 1.0)

    # Link newly created nodes.
    link_new_default_nodes(color_material_channel_node, texture_node, general_nodes)

    # Frame new nodes.
    frame_new_default_nodes(color_material_channel_node, layers, selected_layer_index)
    
    # Update node layer indicies.
    update_layer_nodes.update_layer_node_indicies(context, "COLOR")

def link_new_default_nodes(material_channel_node, texture_node, general_nodes):
    '''Links newly created default nodes together.'''
    link = material_channel_node.node_tree.links.new
    link(texture_node.outputs[0], general_nodes["MIXLAYER"].inputs[1])
    link(general_nodes["OPACITY"].outputs[0], general_nodes["MIXLAYER"].inputs[0])
    link(general_nodes["COORD"].outputs[2], general_nodes["MAPPING"].inputs[0])

def add_general_layer_nodes(material_channel_node, layers, layer_index):
    '''Adds general layer nodes that should be present in all layers.'''

    if material_channel_node == None:
        print("Error: No material channel found.")
        return

    # Create general nodes in the material channel.
    opacity_node = material_channel_node.node_tree.nodes.new(type='ShaderNodeMath')
    mix_layer_node = material_channel_node.node_tree.nodes.new(type='ShaderNodeMixRGB')
    coord_node = material_channel_node.node_tree.nodes.new(type='ShaderNodeTexCoord')
    mapping_node = material_channel_node.node_tree.nodes.new(type='ShaderNodeMapping')

    # Set the nodes default names.
    opacity_node.name = "OPACITY_"
    opacity_node.label = opacity_node.name
    
    mix_layer_node.name = "MIXLAYER_"
    mix_layer_node.label = mix_layer_node.name

    coord_node.name = "COORD_"
    coord_node.label = coord_node.name

    mapping_node.name = "MAPPING_"
    mapping_node.label = mapping_node.name

    # Set node default values.
    opacity_node.inputs[0].default_value = 1.0
    opacity_node.inputs[1].default_value = 1.0
    opacity_node.use_clamp = True
    opacity_node.operation = 'SUBTRACT'
    mix_layer_node.inputs[2].default_value = (0.0, 0.0, 0.0, 1.0)
    mix_layer_node.use_clamp = True

    # Store the node names in the layer so they can be accessed.
    layers[layer_index].opacity_node_name = opacity_node.name
    layers[layer_index].mix_layer_node_name = mix_layer_node.name
    layers[layer_index].coord_node_name = coord_node.name
    layers[layer_index].mapping_node_name = mapping_node.name

    # Return the new nodes.
    general_nodes = {
        "OPACITY": opacity_node,
        "MIXLAYER": mix_layer_node,
        "COORD": coord_node,
        "MAPPING": mapping_node
    }

    return general_nodes

def frame_new_default_nodes(material_channel_node, layers, layer_index):
    '''Creates a layer frame and frames the given nodes.'''

    # Create a layer frame.
    frame = material_channel_node.node_tree.nodes.new(type='NodeFrame')
    frame.name = "NewFrame"
    frame.label = frame.name
    layers[layer_index].frame_name = frame.name

    # Frame all the nodes in the given layer in the newly created frame.
    nodes = layer_nodes.get_all_layer_nodes(material_channel_node, layers, layer_index)
    for n in nodes:
        n.parent = frame