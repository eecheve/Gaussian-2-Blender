import bpy
import sys

from bpy import context
import math
from math import *
import mathutils

def RefineCoordList(list):
    """
    Converts string coordinates to floats for each entry in the list.

    :param list: (list) Each entry is a list of four strings: the symbol and each coordinate in x, y, z.
    :return: (list) Each entry corresponds to an atom symbol and its coordinates.
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
    Refines the connectivity list to ensure each item has at least three elements.

    :param list: (list) Connectivity list where each line has all connect info for one atom.
    :return: (list) List of lists, each item has the numbers of the two atoms involved and the bond type.
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
    Modifies entry list. If an enty inside the list is a string of an int, it becomes an int.

    :param list: (list) List containing string representations of integers.
    :return: (list) List with integers converted from strings.
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
    """
    Adds element symbols to the connectivity list.

    :param connect: (list) Connectivity list.
    :param coords: (list) List of coordinates.
    :param number_of_elements: (int) Number of elements.
    :return: (list) Connectivity list with element symbols added.
    """
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
    Converts a string representation of a list into an actual list of strings.

    :param str_list: (str) String representation of a list.
    :return: (list) List of strings.
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
    Converts a string representation of a tuple into an actual tuple.

    :param str_in: (str) String of the form "(a,b,c)".
    :return: (tuple) Tuple of the form (a, b, c).
    """
    str_in = str_in.strip("()")
    l = str_in.split(",")
    return tuple(l)

def make_tuple_in_list(a_list):
    """
    Converts a list of string representations of tuples into a list of actual tuples.

    :param a_list: (list) List of string representations of tuples.
    :return: (list) List of tuples.
    """
    l = []
    for entry in a_list:
        tup = make_tuple(entry)
        l.append(tup)
    return l

def refine_key_frames(raw_key_frames):
    """
    Refines raw key frames by converting coordinates to vectors.

    :param raw_key_frames: (list) List of raw key frames.
    :return: (list) List of refined key frames with vectors.
    """
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
    """
    Creates a dictionary of key frames with element names as keys and vectors as values.

    :param key_frames: (list) List of key frames.
    :return: (dict) Dictionary of key frames.
    """
    d = {}
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
            d[name] = vector_list
        return d
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
            d[name] = vector_list
        return d
    else:
        print("@Refine_Elements: Too many atoms, cannot process")
        return d