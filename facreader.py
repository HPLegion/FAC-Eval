'''
Functions for importing verbose FAC ASCII Output Files
'''

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
import pandas as pd

def read_ai(filename):
    '''
    Method for Importing a FAC Output containing data on autoionising transitions
    '''
    data = pd.DataFrame()
    with open(filename) as fobj:
        header = read_fac_header(fobj)
        for n in range(header["NBlocks"]):
            block = read_ai_block(fobj)
            block["BLOCK_INDEX"] = n
            data = data.append(block, ignore_index=True)
    return header, data

def read_ai_block(fobj):
    '''
    Reads a block of an ai file and returns a dataframe with the content
    Expects Cursor at beginning of block and moves it past the final newline of this block
    '''
    # Read Block Header
    NELE = int(fobj.readline().split("=")[-1])
    NTRANS = int(fobj.readline().split("=")[-1])
    line = fobj.readline()
    if line.startswith("CHANNE"):
        CHANNEL = int(line.split("=")[-1])
        EMIN = float(fobj.readline().split("=")[-1])
    else:
        CHANNEL = None
        EMIN = float(line.split("=")[-1])
    NEGRID = int(fobj.readline().split("=")[-1])
    EGRID = []
    for _ in range(NEGRID):
        EGRID.append(float(fobj.readline()))

    # Read Block
    block = []
    for _ in range(NTRANS):
        block.append(fobj.readline())

    # Read one more line to move cursor to next block/EOF
    fobj.readline()

    # Convert buffered data to pandas object
    df_names = ["BOUND_ILEV",
                "BOUND_2J",
                "FREE_ILEV",
                "FREE_2J",
                "DELTA_E",
                "AI_RATE",
                "DC_STRENGTH"]
    df_types = {"BOUND_ILEV":int,
                "BOUND_2J":int,
                "FREE_ILEV":int,
                "FREE_2J":int,
                "DELTA_E":float,
                "AI_RATE":float,
                "DC_STRENGTH":float}
    buffer = StringIO("".join(block))
    df = pd.read_csv(buffer, delim_whitespace=True,
                     names=df_names, dtype=df_types, index_col=False)
    buffer.close()

    # Add header data
    df["NELE"] = NELE
    df["NTRANS"] = NTRANS
    df["NEGRID"] = NEGRID
    df["EMIN"] = EMIN
    df['EGRID'] = ", ".join([str(e) for e in EGRID])
    if CHANNEL:
        df["CHANNEL"] = CHANNEL

    return df

def read_tr(filename):
    '''
    Method for Importing a FAC Output containing data on radiative transitions
    '''
    data = pd.DataFrame()
    with open(filename) as fobj:
        header = read_fac_header(fobj)
        for n in range(header["NBlocks"]):
            block = read_tr_block(fobj)
            block["BLOCK_INDEX"] = n
            data = data.append(block, ignore_index=True)
    return header, data

def read_tr_block(fobj):
    '''
    Reads a block of an ai file and returns a dataframe with the content
    Expects Cursor at beginning of block and moves it past the final newline of this block
    '''
    # Read Block Header
    NELE = int(fobj.readline().split("=")[-1])
    NTRANS = int(fobj.readline().split("=")[-1])
    MULTIP = int(fobj.readline().split("=")[-1])
    GAUGE = int(fobj.readline().split("=")[-1])
    MODE = int(fobj.readline().split("=")[-1])

    # Read Block
    block = []
    for _ in range(NTRANS):
        block.append(fobj.readline())

    # Read one more line to move cursor to next block/EOF
    fobj.readline()

    # Convert buffered data to pandas object
    df_names = ["UPPER_ILEV",
                "UPPER_2J",
                "LOWER_ILEV",
                "LOWER_2J",
                "DELTA_E",
                "GF",
                "TR_RATE",
                "MULTIPOLE"]
    df_types = {"UPPER_ILEV":int,
                "UPPER_2J":int,
                "LOWER_ILEV":int,
                "LOWER_2J":int,
                "DELTA_E":float,
                "GF":float,
                "TR_RATE":float,
                "MULTIPOLE":float}
    buffer = StringIO("".join(block))
    df = pd.read_csv(buffer, delim_whitespace=True,
                     names=df_names, dtype=df_types, index_col=False)
    buffer.close()

    # Add header data
    df["NELE"] = NELE
    df["NTRANS"] = NTRANS
    df["MULTIP"] = MULTIP
    df["GAUGE"] = GAUGE
    df["MODE"] = MODE


    return df



def read_fac_header(fobj):
    '''
    Reads the header section of a FAC Output and returns the information in the form of a dict
    Expects Cursor at beginning of header and moves it past the final newline of the header
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


# df_names = ["BOUND_ILEV",
#             "BOUND_2J",
#             "FREE_ILEV",
#             "FREE_2J",
#             "DELTA_E",
#             "AI_RATE",
#             "DC_STRENGTH"]
# df_types = {"BOUND_ILEV":int,
#             "BOUND_2J":int,
#             "FREE_ILEV":int,
#             "FREE_2J":int,
#             "DELTA_E":float,
#             "AI_RATE":float,
#             "DC_STRENGTH":float}
ai_header, ai_data = read_ai("K.li.ai")
tr_header, tr_data = read_tr("K.li.tr")
print(tr_header)
print(tr_data.head())
print("wait")
print("wait")
print("wait")
