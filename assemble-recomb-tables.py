"""
Script that collects all DR relevant Files from a directory and saves a combined recombination
table for each element
"""
##### Imports
import os

import factools.fileimport
import factools.reconstruction
import factools.dr

##### Constants
ELEMENT_Z = {"H":1, "He":2, "Li":3, "Be":4, "B":5, "C":6, "N":7, "O":8, "F":9, "Ne":10, "Na":11,
             "Mg":12, "Al":13, "Si":14, "P":15, "S":16, "Cl":17, "Ar":18, "K":19, "Ca":20, "Sc":21,
             "Ti":22, "V":23, "Cr":24, "Mn":25, "Fe":26, "Co":27, "Ni":28, "Cu":29, "Zn":30,
             "Ga":31, "Ge":32, "As":33, "Se":34, "Br":35, "Kr":36, "Rb":37, "Sr":38, "Y":39,
             "Zr":40, "Nb":41, "Mo":42, "Tc":43, "Ru":44, "Rh":45, "Pd":46, "Ag":47, "Cd":48,
             "In":49, "Sn":50, "Sb":51, "Te":52, "I":53, "Xe":54, "Cs":55, "Ba":56, "La":57,
             "Ce":58, "Pr":59, "Nd":60, "Pm":61, "Sm":62, "Eu":63, "Gd":64, "Tb":65, "Dy":66,
             "Ho":67, "Er":68, "Tm":69, "Yb":70, "Lu":71, "Hf":72, "Ta":73, "W":74, "Re":75,
             "Os":76, "Ir":77, "Pt":78, "Au":79, "Hg":80, "Tl":81, "Pb":82, "Bi":83, "Po":84,
             "At":85, "Rn":86, "Fr":87, "Ra":88, "Ac":89, "Th":90, "Pa":91, "U":92, "Np":93,
             "Pu":94, "Am":95, "Cm":96, "Bk":97, "Cf":98, "Es":99, "Fm":100, "Md":101, "No":102,
             "Lr":103, "Rf":104, "Db":105, "Sg":106, "Bh":107, "Hs":108, "Mt":109, "Ds":110,
             "Rg":111, "Cn":112, "Nh":113, "Fl":114, "Mc":115, "Lv":116, "Ts":117}
CHARGE_STATE = "CHARGE_STATE"

##### Setup Variables
RAWPATH = "./cs/" # Folder to scan for raw data
OUTPATH = "./cs/" # Folder to put the output data
OUTPOSTFIX = "_LMM" # Postfix for the filename --> element + postfix +.csv
VERBOSE = True

##### Helper Methods ----- These may need to be adjusted depending on filenaming conventions
def base_element(fileNameStub): # The element representing the ionic core
    # return fileNameStub.split(".")[0]
    return fileNameStub.split("_")[0]

def remaining_electrons(fileNameStub): # The charge state identification
    # temp = fileNameStub.split(".")[1]
    # temp = temp.split("-")[0]
    temp = fileNameStub.split("-")[1]
    temp = temp.split(".")[0]
    return ELEMENT_Z[temp.capitalize()]

##### Main Script
# Collect a list of all filename stubs, based on all ai files in directory
FILES = [f[:-3] for f in os.listdir(RAWPATH) if f[-3:] == ".ai"] # Get the fname-stub for all cases

# Sort them by the element they belong to
print("Entering directory:", RAWPATH)
FILES_BY_ELEMENT = {}
for f in FILES:
    element = base_element(f)
    if element not in FILES_BY_ELEMENT:
        FILES_BY_ELEMENT[element] = [f,]
    else:
        FILES_BY_ELEMENT[element].append(f)

print("Found the following data sets:")
for element in FILES_BY_ELEMENT:
    print(element, "---", FILES_BY_ELEMENT[element])

# Element by element, go through all related charge states/files
count_attempt = 0
count_success = 0
fails = []
for element, element_files in FILES_BY_ELEMENT.items():
    print("Now processing element:", element)
    element_df = None
    out_file = OUTPATH + element + OUTPOSTFIX + ".csv"

    for f in element_files:
        count_attempt += 1
        print("Filestub:", f)
        # Read FAC Files
        lev_file = RAWPATH + f + ".lev"
        tr_file = RAWPATH + f + ".tr"
        ai_file = RAWPATH + f + ".ai"
        try:
            (_, ai_df) = factools.fileimport.read_ai(ai_file)
            (_, tr_df) = factools.fileimport.read_tr(tr_file)
            (_, lev_df) = factools.fileimport.read_lev(lev_file)
        except:
            fails.append((element, f, "FileError"))
            continue

        # Reconstruct the full level names (NECESSARY STEP)
        try:
            lev_df = factools.reconstruction.amend_level_dataframe(lev_df, verbose=VERBOSE)
        except:
            fails.append((element, f, "ReconstructionError"))
            continue

        # Assemble the data for this element-charge state combination
        try:
            df = factools.dr.dr_recombination_table(lev_df, ai_df, tr_df, verbose=VERBOSE)
        except:
            fails.append((element, f, "DRError"))
            continue

        df[CHARGE_STATE] = ELEMENT_Z[element] - remaining_electrons(f)
        if element_df is None:
            element_df = df
        else:
            element_df = element_df.append(df, ignore_index=True)
        count_success += 1

    element_df.sort_values([CHARGE_STATE, factools.dr.DE_AI], inplace=True)
    element_df.to_csv(out_file, index=False)

print("Done! Successfully processed" , count_success, "of", count_attempt, "data sets:")
if fails:
    print("Failed cases:")
    for fail in fails:
        print(fail)
