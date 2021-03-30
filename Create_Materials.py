import bpy

def CreateAndAssignMaterials(ref_dict):
    """
    ref_dict: Dictionary<string, Atom_Data> elements present in the molecule and their data
    summary: Instantiates the materials for the elements present in the molecule
    """
    d = {}
    for key in ref_dict:
        d[key] = AssignMaterial(key, ref_dict.get(key).get_color()) 
    return d
    

def AssignMaterial(material_name, material_color):
    """
    material_color: Tuple<(float, float, float, int)> RGBA values for material
    summary: If material does not exist: creates it and assigns its name and diffuse color
    returns: material object
    """
    assignment = bpy.data.materials.get(material_name)
    if assignment is None:
        assignment = bpy.data.materials.new(name=material_name)
        assignment.diffuse_color = material_color
    return assignment

def RemoveAllMaterials():
    for m in bpy.data.materials:
        bpy.data.materials.remove(m)
        
RemoveAllMaterials()