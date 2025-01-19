import bpy
import sys
import os

dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir)

import Import_Data

import importlib #<-- for end user in case they want to add functionality. 
importlib.reload(Import_Data)

def Set_Raw_Parameters(i_folder_path, i_file_name):
    """
    Returns: 
        raw_coords: List of lists, each entry has four items, the first is the element name (no index) 
        the remaining three are the cartesian coordinates of such element
        raw_connect: Connectivity information as is extracted from the .com file. The refinement is done
        elsewhere
    """
    file_path = os.path.join(i_folder_path, i_file_name)
    raw_data = Import_Data.ExtractDataFromFile(file_path)
    raw_data = Import_Data.FilterOutExtraInformation('above', 2, 1, raw_data) #removes everything above the second line break +1 line, from the raw_data
    raw_data = Import_Data.FilterOutExtraInformation('below', 2, 1, raw_data) #raw coords and connectivity.
    print("2: Extracting information from .com file ...")
    raw_coords = Import_Data.FilterOutExtraInformation('below', 1, 1, raw_data)
    raw_connect = Import_Data.FilterOutExtraInformation('above', 1, 0, raw_data)
    return raw_coords, raw_connect
        
def split_coord_frames(raw_coord_frames):
    l = []
    m = []
    frame_count = count_animation_frames(raw_coord_frames)
    for coord_frame in raw_coord_frames:
        n = []
        o = []
        o.append(coord_frame[0]) #to assign the element
        for i in range(4):
            n.append(coord_frame[i]) #assigning first xyz coords to element
        l.append(n)
        for j in range(1, frame_count + 1):
            right = (j*3) + 1 #x coordinate index for frame j
            for k in range(3):
                coord = coord_frame[right+k] #each of the three coordinates for frame j
                o.append(coord)
        m.append(o)
    return l, m
        
def count_animation_frames(raw_coord_frames):
    first_element = raw_coord_frames[0]
    total_frames = (len(first_element) - 1)/3 #first entry is element symbol, each following 3 are x y z.
    return int(total_frames - 1) #because the first frame will be used to build the molecule.