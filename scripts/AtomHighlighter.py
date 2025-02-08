import bpy
import math

def hex_to_rgba(hex_color):
    """
    Converts a hex color string to an RGBA list, supporting optional alpha.

    Param: hex_color (str): A string representing the hex color (e.g., "#ea1517" or "#ea151780").

    Returns:
        list: A list of four float values representing the RGBA color.
    """
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 6:  # No alpha
        return [int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4)] + [1.0]
    elif len(hex_color) == 8:  # Includes alpha
        return [int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4, 6)]
    else:
        raise ValueError("Invalid hex color format. Use #RRGGBB or #RRGGBBAA.")

def find_bond_object(atom1, atom2):
    """
    Finds the bond object in the scene that contains atom1 and atom2 in its name.

    Parameters:
    atom1 (str): The name and index of the first atom (e.g., "C01").
    atom2 (str): The name and index of the second atom (e.g., "C02").

    Returns:
    bpy.types.Object: The bond object if found, None otherwise.
    """
    separators = ['-', '=', '#', '%', '_']
    for obj in bpy.data.objects:
        for sep in separators:
            if f"{atom1}{sep}{atom2}" in obj.name or f"{atom2}{sep}{atom1}" in obj.name:
                return obj
    return None

def highlight_atom(atom_name, outline_size=1.5, transparency_value=0.5, outline_color="#15eae333"):
    """
    Highlights an atom by creating a highlight sphere around it.

    Parameters:
    object_name (str): The name of the atom object to highlight.
    outline_size (float): The size multiplier for the outline sphere relative to the atom object (default is 1.5).
    transparency_value (float): The transparency value for the outline material (default is 0.5).
    outline_color (str): The color of the outline in hex format (e.g., "#15eae3").
    """
    # Try to get the object with the name atom_name
    obj = bpy.data.objects.get(atom_name)
    if obj is None:
        print(f"Error: Object with name '{atom_name}' not found.")
        return
    
    # Create the highlight sphere
    bpy.ops.mesh.primitive_uv_sphere_add(radius=outline_size * obj.dimensions[0] / 2, location=obj.location)
    highlight_sphere = bpy.context.object
    highlight_sphere.name = f"{atom_name}_highlight"
    bpy.ops.object.shade_smooth() # Apply smooth shading
    
    # Make the instantiated object a child of the selected object
    highlight_sphere.parent = obj
    highlight_sphere.location = (0, 0, 0)
    
    # Create the highlight material
    mat = create_highlight_material(atom_name, transparency_value, outline_color)
    
    # Assign the material to the instantiated object
    highlight_sphere.data.materials.append(mat)
    
def create_highlight_material_old(object_name, transparency_value=0.5, outline_color="#15eae3"):
    """
    Creates a highlight material with proper transparency handling.

    Parameters:
    object_name (str): The name of the object to highlight.
    transparency_value (float): The transparency value for the outline material (default is 0.5).
    outline_color (str): The color of the outline in hex format (e.g., "#15eae3").

    Returns:
    bpy.types.Material: The created highlight material.
    """
    mat = bpy.data.materials.new(name=f"{object_name}_highlight")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # Clear default nodes
    for node in nodes:
        nodes.remove(node)

    # Add new nodes
    output_node = nodes.new(type='ShaderNodeOutputMaterial')
    transparent_node = nodes.new(type='ShaderNodeBsdfTransparent')
    emission_node = nodes.new(type='ShaderNodeEmission')
    mix_node = nodes.new(type='ShaderNodeMixShader')
    transparency_value_node = nodes.new(type='ShaderNodeValue')

    # Set color and transparency correctly
    rgba_color = hex_to_rgba(outline_color)  # Ensure this correctly extracts transparency
    emission_node.inputs['Color'].default_value = rgba_color  # Ensure alpha is included
    transparency_value_node.outputs[0].default_value = transparency_value  # Control transparency

    # Link nodes correctly
    links.new(transparency_value_node.outputs[0], mix_node.inputs[0])  # Mix factor
    links.new(transparent_node.outputs['BSDF'], mix_node.inputs[1])  # Transparent path
    links.new(emission_node.outputs['Emission'], mix_node.inputs[2])  # Emission path
    links.new(mix_node.outputs[0], output_node.inputs[0])  # Final shader output

    # Enable proper material transparency settings
    mat.blend_method = 'BLEND'
    mat.shadow_method = 'NONE'
    mat.use_backface_culling = False  # Important for correct rendering
    mat.show_transparent_back = True  # Ensures backface transparency in Eevee

    # Set viewport display properties
    mat.diffuse_color = rgba_color

    return mat

def create_highlight_material(object_name, transparency_value=0.5, outline_color="#15eae3"):
    """
    Creates a highlight material with the specified transparency and outline color.

    Parameters:
    object_name (str): The name of the object to highlight.
    transparency_value (float): The transparency value for the material (default is 0.5).
    outline_color (str): The color of the outline in hex format (e.g., "#15eae3").

    Returns:
    bpy.types.Material: The created highlight material.
    """
    mat = bpy.data.materials.new(name=f"{object_name}_highlight")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # Clear default nodes
    for node in nodes:
        nodes.remove(node)

    # Add necessary nodes
    output_node = nodes.new(type='ShaderNodeOutputMaterial')
    principled_node = nodes.new(type='ShaderNodeBsdfPrincipled')

    # Set base color and transparency
    base_color = hex_to_rgba(outline_color)
    base_color[3] = transparency_value  # Apply alpha value

    principled_node.inputs['Base Color'].default_value = base_color
    principled_node.inputs['Alpha'].default_value = transparency_value

    # Link nodes
    links.new(principled_node.outputs['BSDF'], output_node.inputs['Surface'])

    # Set transparency settings for proper viewport display
    mat.blend_method = 'BLEND'
    mat.shadow_method = 'NONE'
    mat.use_backface_culling = True

    return mat
    
def highlight_bond(atom_1, atom_2, outline_size=0.33, transparency_value=0.5, outline_color="#15eae3"):
    """
    Highlights a bond by creating a highlight cylinder around it.

    Parameters:
    atom_1 (str): The name and index of the first atom (e.g., "C01").
    atom_2 (str): The name and index of the second atom (e.g., "C02").
    outline_size (float): The size multiplier for the outline cylinder relative to the bond (default is 0.3).
    transparency_value (float): The transparency value for the outline material (default is 0.5).
    outline_color (str): The color of the outline in hex format (e.g., "#15eae3").

    Returns:
    None
    """
    # Find the bond object
    bond_obj = find_bond_object(atom_1, atom_2)
    if bond_obj is None:
        print(f"Error: Bond between '{atom_1}' and '{atom_2}' not found.")
        return
    
    # Get the locations of the atoms
    loc1 = bpy.data.objects[atom_1].location
    loc2 = bpy.data.objects[atom_2].location
    
    # Calculate bond location and orientation
    bond_loc = (loc1 + loc2) / 2
    bond_orientation = loc2 - loc1
    
    try:
        phi = math.atan2(bond_orientation.y, bond_orientation.x)
    except ValueError:
        phi = math.pi / 2
    try:
        theta = math.acos(bond_orientation.z / bond_orientation.length)
    except ValueError:
        theta = 0
    
    # Create the highlight cylinder
    bpy.ops.mesh.primitive_cylinder_add(radius=outline_size / 2, depth=bond_orientation.length, location=bond_loc)
    highlight_cylinder = bpy.context.object
    highlight_cylinder.name = f"{atom_1}_{atom_2}_highlight"
    bpy.ops.object.shade_smooth() # Apply smooth shading
    
    # Set the rotation of the cylinder
    highlight_cylinder.rotation_euler[1] = theta
    highlight_cylinder.rotation_euler[2] = phi
    
    # Create the highlight material
    mat = create_highlight_material(f"{atom_1}_{atom_2}", transparency_value, outline_color)
    
    # Assign the material to the instantiated object
    highlight_cylinder.data.materials.append(mat)
    
    # Set the parent of the highlight cylinder to the bond object
    highlight_cylinder.parent = bond_obj
    
    # Ensure the highlight cylinder retains its location and rotation
    highlight_cylinder.matrix_parent_inverse = bond_obj.matrix_world.inverted()
        
#TO DEBUG
#mat_dict = {'C': bpy.data.materials['C'], 'S': bpy.data.materials['S'], 'O': bpy.data.materials['O'], 'H': bpy.data.materials['H'], 'Xx': bpy.data.materials['Xx']}

#highlight_atom(atom_name="C01", transparency_value=0.2)
#highlight_atom(atom_name="O04", transparency_value=0.2)
#highlight_bond(atom_1="C01", atom_2="O04", transparency_value=0.2, outline_size=0.33)