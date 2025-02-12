import bpy
import math

def hex_to_rgba(hex_color):
    """
    Converts a hex color string to an RGBA list, supporting optional alpha.

    :param hex_color: (str) A string representing the hex color (e.g., "#ea1517" or "#ea151780").
    :return: A list of four float values representing the RGBA color.
    :rtype: [float, float, float, float]
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

    :param atom1: (str) The name and index of the first atom (e.g., "C01").
    :param atom2: (str) The name and index of the second atom (e.g., "C02").
    :return: The bond object if found, None otherwise.
    :rtype: bpy.types.Object or None
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

    :param atom_name: (str) The name of the atom object to highlight.
    :param outline_size: (float) The size multiplier for the outline sphere relative to the atom object (default is 1.5).
    :param transparency_value: (float) The transparency value for the outline material (default is 0.5).
    :param outline_color: (str) The color of the outline in hex format (default is "#15eae3").
    """
    # Try to get the object with the name atom_name
    obj = bpy.data.objects.get(atom_name)
    if obj is None:
        print(f"Error: Object with name '{atom_name}' not found.")
        return
    
    # Create the highlight sphere
    bpy.ops.mesh.primitive_uv_sphere_add(radius=outline_size * obj.dimensions[0] / 2, location=obj.location)
    highlight_sphere = bpy.context.object
    highlight_sphere.name = f"{atom_name}*highlight" #naming format with '*' to avoid interverence with animate module
    bpy.ops.object.shade_smooth() # Apply smooth shading
    
    # Make the instantiated object a child of the selected object
    highlight_sphere.parent = obj
    highlight_sphere.location = (0, 0, 0)
    
    # Create the highlight material
    mat = create_highlight_material(atom_name, transparency_value, outline_color)
    
    # Assign the material to the instantiated object
    highlight_sphere.data.materials.append(mat)
    
def create_highlight_material(object_name, transparency_value=0.5, outline_color="#15eae3"):
    """
    Creates a highlight material with the specified transparency and outline color.

    :param object_name: (str) The name of the object to highlight.
    :param transparency_value: (float) The transparency value for the material (default is 0.5).
    :param outline_color: (str) The color of the outline in hex format (default is "#15eae3").
    :return: The created highlight material.
    :rtype: bpy.types.Material
    """
    mat = bpy.data.materials.new(name=f"{object_name}*highlight")
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

    :param atom_1: (str) The name and index of the first atom (e.g., "C01").
    :param atom_2: (str) The name and index of the second atom (e.g., "C02").
    :param outline_size: (float) The size multiplier for the outline cylinder relative to the bond (default is 0.33).
    :param transparency_value: (float) The transparency value for the outline material (default is 0.5).
    :param outline_color: (str) The color of the outline in hex format (default is "#15eae3").
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
    highlight_cylinder.name = f"{atom_1}*{atom_2}*highlight"
    bpy.ops.object.shade_smooth() # Apply smooth shading
    
    # Set the rotation of the cylinder
    highlight_cylinder.rotation_euler[1] = theta
    highlight_cylinder.rotation_euler[2] = phi
    
    # Create the highlight material
    mat = create_highlight_material(f"{atom_1}*{atom_2}", transparency_value, outline_color)
    
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