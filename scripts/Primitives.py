import bpy

from bpy import context
import math
from math import *
import mathutils

def InstantiateElementsFromDictionary(pos_dict, element_data, materials_dict, van_der_waals = False):
    """
    pos_dict: Dictionary<string, Vector3> all the symbols & labels of elements and their Vector3 positions
    element_data: Dictionary<string, Atom_Data(class)> available data for the present elements
    materials_dict: Dictionary<string, bpy.Material> materials that can be accessed with present elements' symbols
    summary: instantiates spheres of different radii & materials at the allocated Vector3 positions.
    """
    for key in pos_dict:
        e_symbol = ''.join(i for i in key if not i.isdigit()) #remove numbers from name
        if e_symbol in element_data:
            if van_der_waals == False:
                 r = element_data.get(e_symbol).get_radius() / 2
            else:
                 r = element_data.get(e_symbol).get_vanDerWaals()
            x = pos_dict[key].x
            y = pos_dict[key].y
            z = pos_dict[key].z
            bpy.ops.mesh.primitive_uv_sphere_add(enter_editmode=False, location=(x, y, z), radius=r)
            ModifyNamesAndMaterials(key, e_symbol, materials_dict)
            bpy.ops.object.shade_smooth()
            print("6: Instantiating element: ", key)
        else:
            print("AddElement(): invalid element name")
            
def InstantiateIonsFromDictionary(pos_dict, ion_data, materials_dict):
    for key in pos_dict:
        i_symbol = ''.join(i for i in key if not i.isdigit()) #remove numbers from name
        if i_symbol in ion_data:
            r = ion_data[i_symbol].radius /2
            x = pos_dict[key].x
            y = pos_dict[key].y
            z = pos_dict[key].z
            bpy.ops.mesh.primitive_uv_sphere_add(enter_editmode=False, location=(x, y, z), radius=r)
            ModifyNamesAndMaterials(key, i_symbol, materials_dict)
            bpy.ops.object.shade_smooth()
            print("6: Instantiating ion: ", key)
        else:
            print("AddElement(): invalid element name")
                    
def ModifyNamesAndMaterials(obj_name, e_symbol, materials_dict):
    """
    obj_name: <string> the name of the sphere to be instantiated
    e_symbol: atom symbol, taken from name, used to access materials
    materials_dict: Dictionary<string, bpy.Material> materials that can be accessed with present elements' symbols
    summary: Changes names of the active object and appends to it the required material.
    """
    bpy.context.active_object.name = obj_name
    bpy.context.active_object.data.name = obj_name
    mat = materials_dict.get(e_symbol)
    try:
        bpy.context.active_object.data.materials.append(mat)
    except:
        print("6: Material not found @Primitives.ModifyNamesAndMaterials")
    
def InstantiateBondsFromConnectivity(pos_dict, mat_dict, connect_list, unit_cell="0"):
    for item in connect_list:
        atom1 = item[0]
        atom2 = item[1]
        bond_type = item[2]
        print("6: Instantiating bond: ", atom1+bond_type+atom2)
        if bond_type == '_':
            if unit_cell == "0":
                CreateAndJoinTrantientBond(pos_dict, mat_dict, atom1, atom2, '_', 0.2, 0.06, h_bonding=True)
            else:
                CreateFragmentedBonds(pos_dict, mat_dict, atom1, atom2, bond_type, unit_cell)
        elif bond_type == '-':
            bond_label = atom1 + '-' + atom2
            bond_label2 = atom2 + '-' + atom1
            CreateFragmentedBonds(pos_dict, mat_dict, atom1, atom2, bond_type)
            SelectTwoMeshesAndJoin(bond_label, bond_label2)
        elif bond_type == '=':
            bond_label = atom1 + '=' + atom2
            bond_label2 = atom2 + '=' + atom1
            CreateFragmentedBonds(pos_dict, mat_dict, atom1, atom2, bond_type)
            CreateFragmentedBonds(pos_dict, mat_dict, atom1, atom2, bond_type)
            MoveObjectOnLocalAxis(bond_label,(0.0,0.1,0.0))
            MoveObjectOnLocalAxis(bond_label2,(0.0,0.1,0.0))
            MoveObjectOnLocalAxis(bond_label+".001",(0.0,-0.1,0.0))
            MoveObjectOnLocalAxis(bond_label2+".001",(0.0,-0.1,0.0))
            SelectTwoMeshesAndJoin(bond_label, bond_label2)
            SelectTwoMeshesAndJoin(bond_label+".001", bond_label2+".001")
            SelectTwoMeshesAndJoin(bond_label, bond_label+".001")
        elif bond_type == 'res1':
            bond_label = atom1 + '-=' + atom2
            bond_label2 = atom2 + '-=' + atom1
            bond_label3 = atom1 + '=-' + atom2 + ".001"
            CreateFragmentedBonds(pos_dict, mat_dict, atom1, atom2, '-=')
            MoveObjectOnLocalAxis(bond_label,(0.0,0.1,0.0))
            MoveObjectOnLocalAxis(bond_label2,(0.0,0.1,0.0))
            SelectTwoMeshesAndJoin(bond_label, bond_label2)
            CreateAndJoinTrantientBond(pos_dict, mat_dict, atom1, atom2, '=-', 0.18, 0.08)
            MoveObjectOnLocalAxis(bond_label3,(0.0,-0.1,0.0))
            SelectTwoMeshesAndJoin(bond_label, bond_label3)
        elif bond_type == '#':
            bond_label = atom1 + '#' + atom2
            bond_label2 = atom2 + "#" + atom1
            CreateFragmentedBonds(pos_dict, mat_dict, atom1, atom2, bond_type)
            CreateFragmentedBonds(pos_dict, mat_dict, atom1, atom2, bond_type)
            CreateFragmentedBonds(pos_dict, mat_dict, atom1, atom2, bond_type)
            MoveObjectOnLocalAxis(bond_label+".001",(0.0,0.15,0.0))
            MoveObjectOnLocalAxis(bond_label+".002",(0.0,-0.15,0.0))
            MoveObjectOnLocalAxis(bond_label2+".001",(0.0,0.15,0.0))
            MoveObjectOnLocalAxis(bond_label2+".002",(0.0,-0.15,0.0))
            SelectTwoMeshesAndJoin(bond_label, bond_label2)
            SelectTwoMeshesAndJoin(bond_label+".001", bond_label2+".001")
            SelectTwoMeshesAndJoin(bond_label+".002", bond_label2+".002")
            SelectTwoMeshesAndJoin(bond_label+".001", bond_label+".002")
            SelectTwoMeshesAndJoin(bond_label+".001", bond_label2)
        else:
            print("Error on bond type! @Primitives.InstantiateBondsFromConnectivity")
            
def CreateAndJoinTrantientBond(pos_dict, mat_dict, key1, key2, bond_type, dash_len, bond_radius, h_bonding=False): 
    scene = bpy.context.scene
    #temporary names for the bonds instantiated
    name1 = key1 + bond_type + key2
    name2 = key2 + bond_type + key1
    #spawn positions for elements, their distance and how many dashes the bond would have
    origin = pos_dict.get(key1)
    end = pos_dict.get(key2)
    vector = end - origin
    distance = vector.magnitude
    normal_vector = vector / distance
    dash_nmbr = int(distance/dash_len) #number of times dash_len fits in distance.
    ref_nmbr = int(dash_nmbr/2) #middle point in the number of dashes
    #elements taken from names by removing numerical part
    type1 = ''.join(i for i in key1 if not i.isdigit())
    type2 = ''.join(i for i in key2 if not i.isdigit())
    #instantiating dashes between spawn points and mid point
    for i in range(dash_nmbr):
        if i != 0 and i % 2 == 0: #will instantiate dashes only in half of the spaces 
            mid_point = (normal_vector * dash_len * i) + origin
            bpy.ops.mesh.primitive_cylinder_add(radius=bond_radius, depth=dash_len, enter_editmode=False, location=mid_point)
            try:
                phi = math.atan2(vector.y, vector.x)
            except ValueError:
                phi = math.pi / 2
            try:
                theta = math.acos(vector.z/distance)
            except ValueError:
                theta = 0
            bpy.context.object.rotation_euler[1] = theta #dash orientation management
            bpy.context.object.rotation_euler[2] = phi
            if h_bonding == False:
                if i <= ref_nmbr: #dashes closest to atom 1
                    ModifyNamesAndMaterials(name1, type1, mat_dict)
                else: #dashes closest to atom 2
                    ModifyNamesAndMaterials(name1, type2,  mat_dict)
            else:
                ModifyNamesAndMaterials(name1, "Xx", mat_dict) #For trantient or hydrogen bonding
    #getting all the objects with name that starts with name1
    name1_objs = [o for o in scene.objects if o.name.startswith(name1)]
    JoinMeshesFromObjectList(name1_objs)

def CreateFragmentedBonds(pos_dict, mat_dict, atom1, atom2, bond_type, unit_cell="0"):
    """
    pos_dict: Dictionary<string, Vector3>: atomic symbols and their positions
    mat_dict: Dictionary<string, bpy.Material>: atomic symbols and their materials
    atom1: <string>: symbol & number for atom to join 1
    atom2: <string>: symbol & number for atom to join 2
    bond_type: <string>: either single, double or triple
    summary: instantiates bonds from atoms to middle-point and joins them
    """
    #temporary names for the bonds instantiated
    name1 = atom1 + bond_type + atom2
    name2 = atom2 + bond_type + atom1
    #spawn positions for elements and their middle point
    v1 = pos_dict.get(atom1)
    v3 = pos_dict.get(atom2)
    v2 = (v1+v3)/2
    #elements taken from names by removing numerical part
    element1 = ''.join(i for i in atom1 if not i.isdigit())
    element2 = ''.join(i for i in atom2 if not i.isdigit())
    #instantiating bonds and assigning materials and names
    if unit_cell == "0":
        InstantiateBondBetweenTwoPoints(v1, v2)
        ModifyNamesAndMaterials(name1, element1, mat_dict)
        InstantiateBondBetweenTwoPoints(v2, v3)
        ModifyNamesAndMaterials(name2, element2, mat_dict)  
    else:
        InstantiateBondBetweenTwoPoints(v1, v2, 0.03)
        ModifyNamesAndMaterials(name1, "Xx", mat_dict)
        InstantiateBondBetweenTwoPoints(v2, v3, 0.03)
        ModifyNamesAndMaterials(name2, "Xx", mat_dict)
        
def MoveObjectOnLocalAxis(obj_name, value):
    obj = bpy.data.objects[obj_name]
    distz = mathutils.Vector(value)
    rotationMAT = obj.rotation_euler.to_matrix()
    rotationMAT.invert()
    zVector = distz @ rotationMAT # project the vector to the world using the rotation matrix
    obj.location += zVector
    
def InstantiateBondBetweenTwoPoints(p1, p2, r=0.06): #p1 and p2 are the origin and end points
    v = p2 - p1 #vector between the two points
    d = v.magnitude
    m_p = (p1+p2)/2 #midpoint between p1 and p2
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=d, enter_editmode=False, location=m_p)
    try:
        phi = math.atan2(v.y, v.x) #returns a bug if phi is 90 degrees, as tan(90) is not defined
    except ValueError:
        phi = math.pi/2 #to handle the 90 degrees exception
    try:
        theta = math.acos(v.z/d) #returns a bug if theta is 0 degrees
    except ValueError:
        theta = 0
    bpy.context.object.rotation_euler[1] = theta
    bpy.context.object.rotation_euler[2] = phi 
    
def SelectTwoMeshesAndJoin(name1, name2):
    #print("@Primitives_SelectTwoMeshes: selecting",name1,name2)
    obs = []
    scene = bpy.context.scene
    for ob in scene.objects:
        if ob.name == name1 or ob.name == name2:
            if ob.type == 'MESH':
                obs.append(ob)
                #print("@Primitives_selectTwoMeshes: appending",ob.name)
    ctx = bpy.context.copy()
    ctx['active_object'] = obs[0]
    ctx['selected_editable_objects'] = obs
    bpy.ops.object.join(ctx)
    
def JoinMeshesFromObjectList(obj_list):
    ctx = bpy.context.copy()
    ctx['active_object'] = obj_list[0]
    ctx['selected_editable_objects'] = obj_list
    bpy.ops.object.join(ctx)
    
#def EraseDummyAtoms():
#    obs = []
#    scene = bpy.context.scene
#    for ob in scene.objects:
#        if 
