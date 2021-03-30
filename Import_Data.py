import bpy

#---------------------------------------------------------------------------------------------
def ExtractDataFromFile(path):
    """
    path: <string> path to read the file
    returns: a list of data. Each entry corresponds to a line in the file to read
    """
    l = []
    with open(path) as f:
        content = f.readlines()
        for line in content:
            # store the line as list in file_data
            l.append(line.split())
    return l

def FilterOutExtraInformation(spec, line_break_nmbr, extra_nmbr, raw_data): #removes everything after the second line break from the .com file.
    """
    spec: <string> can be either 'above' or 'below'
    line_break_nmbr: <int> will remove everything above or below that number of line breaks, depending of spec
    extra_nmbr: <int> will remove an extra number of lines according to what's needed
    raw_data: <[[values]]> data matrix to filter
    returns: data matrix without the info bedore or after a specific number of line breaks.
    """
    if spec == 'above':
        l = []
        i = 0
        j = 0
        for line in raw_data:
            j = j + 1
            if len(line) == 0:
                i = i + 1
                if i == line_break_nmbr:
                    break
        l = raw_data[j+extra_nmbr:]
        return l
    elif spec == 'below':
        l = []
        i = 0
        j = 0
        for line in raw_data:
            j = j + 1
            if len(line) == 0:
                i = i + 1
                if i == line_break_nmbr:
                    break
        l = raw_data[:j-extra_nmbr]
        return l
    else:
        print('invalid specification')
#-----------------------------------------------------------------------------------------------
