'''
Functions for importing verbose FAC ASCII Output Files
'''

import pandas as pd

def read_ai(filename):
    '''
    Method for Importing a FAC Output containing data on autoionising transitions
    '''
    data = pd.DataFrame()
    with open(filename) as fobj:
        header = read_fac_header(fobj)
    
    return header




def read_fac_header(fobj):
    '''
    Reads the header section of a FAC Output and saved the information in the form of a dict
    '''
    header = dict()

    #Read FAC Version String
    header["Version"] = fobj.readline().strip()

    while True:
        line = fobj.readline()

        # Break on line after header (empty line)
        if line.strip() == '':
            break

        # Break line into key and value
        key = line.split("=", 1)[0].strip()
        val = line.split("=", 1)[1].strip()

        # Try casting value to int then if fails try float
        try:
            val = int(val)
        except ValueError:
            try:
                val = float(val)
            except ValueError:
                pass

        # Treat Element Line specially
        if key.endswith(" Z"):
            header["Z"] = val
            header["Element"] = key[:-2]
        # Otherwise write key value pair to dict
        else:
            header[key] = val

    return header


print(read_ai("K.li.ai"))