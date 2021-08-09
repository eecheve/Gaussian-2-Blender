import bpy
import sys

from bpy import context
import math
from math import *
import mathutils

def RefineCoordList(list):
    """
    input: each entry on list is a list of four strings: the symbol and eac coordinate in x y z
    summary: tries to convert string into float for each entry
    output: each entry corresponds to an atom symbol and its coordinates
    """
    l = []
    for item in list:
        m = []
        for value in item:
            try:
                m.append(float(value))
            except:
                m.append(value)
        l.append(m)
    return l

def RefineConnectivity(list):
    """
    input: connectivity list where each line has all connect info for that one atom
    summary: items in initial list must have at least 3 elements for them to be 
    output: list of lists, each item in list has the numbers of the two atoms involved and the bond type.
    """ 
    l = []
    m = []
    for item in list: 
        if len(item) == 3:
            l.append(item)
        elif len(item) > 3:
            l.append([item[0], item[1], item[2]])
            n = len(item)
            while n - 2 > 2:
                n = n - 2
                value = [item[0], item[n], item[n+1]]
                l.append(value)
    for item in l: #replaces numerical label for bond type with own text-type label
        if item[2] == '0.5':
            item[2] = '_' #transition bond
        elif item[2] == '1.0':
            item[2] = '-' #single bond
        elif item[2] == '1.5':
            item[2] = 'res1' #resonance bond 1: between double & single
        elif item[2] == '2.0':
            item[2] = '=' #double bond
        elif item[2] == '2.5':
            item[2] = 'res2' #resonance bond 2: between double & triple
        elif item[2] == '3.0':
            item[2] = '#' #triple bond
    m = ConvertStringToIndexInList(l)
    return m

def ConvertStringToIndexInList(list):
    """
    if an enty inside the list is a string of an int, it becomes an int.
    """
    l = []
    for item in list:
        m = []
        for value in item:
            try:
                m.append(int(value))
            except:
                m.append(value)
        l.append(m)
    return l

def AddElementSymbolsToConnecrivityList(connect, coords, number_of_elements):
    l = []
    if number_of_elements < 100:
        for entry in connect:
            index1 = entry[0] - 1
            if index1 < 9:
                label1 = '0' + str(index1 + 1)
            else:
                label1 = str(index1 + 1)
            atom1 = str(coords[index1][0]) + label1
            index2 = entry[1] - 1
            if index2 < 9:
                label2 = '0' + str(index2 + 1)
            else:
                label2 = str(index2 + 1)
            atom2 = str(coords[index2][0]) + label2
            l.append([atom1, atom2, entry[2]])
        return l
    elif number_of_elements < 1000:
        for entry in connect:
            index1 = entry[0] - 1
            if index1 < 9:
                label1 = '00' + str(index1 + 1)
            elif index1 < 99:
                label1 = '0' + str(index1 + 1)
            else:
                label1 = str(index1 + 1)
            atom1 = str(coords[index1][0]) + label1
            index2 = entry[1] - 1
            if index2 < 9:
                label2 = '00' + str(index2 + 1)
            elif index2 < 99:
                label2 = '0' + str(index2 + 1)
            else:
                label2 = str(index2 + 1)
            atom2 = str(coords[index2][0]) + label2
            l.append([atom1, atom2, entry[2]])
        return l
    else:
        print("@Refine_Data: More than 1000 elements, cannot process")
        return l

def rebuild_list(str_list):
    """
    takes a string of the list, and returns a list of strings
    """
    k = str_list.split("_")
    str_in = ""
    l = []
    for i in range(len(k)):
        str_in += k[i]
        str_in += ","
        if ')' in k[i]:
            str_in = str_in[:-1]
            l.append(str_in)
            str_in = ""
    return l

def make_tuple(str_in):
    """
    makes a tuple out of a string of the form "(a,b,c)"
    """
    str_in = str_in.strip("()")
    l = str_in.split(",")
    return tuple(l)

def make_tuple_in_list(a_list):
    l = []
    for entry in a_list:
        tup = make_tuple(entry)
        l.append(tup)
    return l

def refine_key_frames(raw_key_frames):
    raw = RefineCoordList(raw_key_frames)
    m = []
    count = len(raw[0])
    for entry in raw:
        l = []
        l.append(entry[0])
        for i in range(1, count, 3):
            x = entry[i]
            y = entry[i+1]
            z = entry[i+2]
            vector = mathutils.Vector((x,y,z))
            l.append(vector)
        m.append(l)
    return m

def create_frames_dict(key_frames):
    dict = {}
    number_of_elements = len(key_frames)
    if number_of_elements < 100:
        for i in range(len(key_frames)):
            if i < 9:
                name = key_frames[i][0] + '0' + str(i+1)
            else:
                name = key_frames[i][0] + str(i+1)
            vector_list = []
            for j in range(1, len(key_frames[i])):
                vector_list.append(key_frames[i][j])
            dict[name] = vector_list
        return dict
    elif number_of_elements < 1000:
        for i in range(len(key_frames)):
            if i < 9:
                name = list[i][0] + '00' + str(i+1)
            elif i < 99:
                name = list[i][0] + '0' + str(i+1)
            else:
                name = list[i][0] + str(i+1)
            vector_list = []
            for j in range(1, len(key_frames[i])):
                vector_list.append(key_frames[i][j])
            dict[name] = vector_list
        return dict
    else:
        print("@Refine_Elements: Too many atoms, cannot process")
        return dict