from pfac import fac
import os

def compute_dr(z, dr_type, path=""):
    elem = fac.ATOMICSYMBOL[z]
    # Initialise
    fac.Reinit()
    fac.SetAtom(elem)
    # Execute problem specific configuration
    type_name = dr_type()
    # Generate filenames
    f_str = path + elem + "_" + type_name
    f_lev = f_str + ".lev"
    f_lev_b = f_lev + ".b" # temp binary
    f_tr = f_str + ".tr"
    f_tr_b = f_tr + ".b" # temp binary
    f_ai = f_str + ".ai"
    f_ai_b = f_ai + ".b" # temp binary
    # Start solving
    fac.ConfigEnergy(0)
    fac.OptimizeRadial(["initial"])
    fac.ConfigEnergy(1)
    # Compute structure and energy levels
    fac.Structure(f_lev_b,["initial", "transient", "final"])
    fac.MemENTable(f_lev_b)
    fac.PrintTable(f_lev_b, f_lev, 1)
    # Compute the transisiton table for radiative decay
    fac.TransitionTable(f_tr_b, ["final"], ["transient"])
    fac.PrintTable(f_tr_b, f_tr, 1)
    # Compute the Autoionisation table
    fac.AITable(f_ai_b, ["transient"], ["initial"])
    fac.PrintTable(f_ai_b, f_ai, 1)
    # Clean up
    for f in [f_lev_b, f_tr_b, f_ai_b]:
        try:
            os.remove(f)
        except OSError as e:  ## if failed, report it back to the user ##
            print("Error: %s - %s." % (e.filename, e.strerror))
    print("Element:" + elem + " DR: " + type_name + " done.")

def compute_kll(z, path=""):
    if z > 2:
        compute_dr(z, kll_he, path)
    if z > 3:
        compute_dr(z, kll_li, path)
    if z > 4:
        compute_dr(z, kll_be, path)
    if z > 5:
        compute_dr(z, kll_b, path)
    if z > 6:
        compute_dr(z, kll_c, path)
    if z > 7:
        compute_dr(z, kll_n, path)
    if z > 8:
        compute_dr(z, kll_o, path)

def compute_klm(z, path=""):
    if z > 2:
        compute_dr(z, klm_he, path)
    if z > 3:
        compute_dr(z, klm_li, path)
    if z > 4:
        compute_dr(z, klm_be, path)
    if z > 5:
        compute_dr(z, klm_b, path)
    if z > 6:
        compute_dr(z, klm_c, path)
    if z > 7:
        compute_dr(z, klm_n, path)
    if z > 8:
        compute_dr(z, klm_o, path)

###### KLL Settings
def kll_he():
    """Electron config for KLL DR with he-like initial state"""
    fac.Config('1s2 2*0', group="initial")
    fac.Config('1*1 2*2', group="transient")
    fac.Config('1s2 2*1', group="final")
    return "KLL-He"

def kll_li():
    """Electron config for KLL DR with li-like initial state"""
    fac.Config('1s2 2*1', group="initial")
    fac.Config('1*1 2*3', group="transient")
    fac.Config('1s2 2*2', group="final")
    return "KLL-Li"

def kll_be():
    """Electron config for KLL DR with be-like initial state"""
    fac.Config('1s2 2*2', group="initial")
    fac.Config('1*1 2*4', group="transient")
    fac.Config('1s2 2*3', group="final")
    return "KLL-Be"

def kll_b():
    """Electron config for KLL DR with b-like initial state"""
    fac.Config('1s2 2*3', group="initial")
    fac.Config('1*1 2*5', group="transient")
    fac.Config('1s2 2*4', group="final")
    return "KLL-B"

def kll_c():
    """Electron config for KLL DR with c-like initial state"""
    fac.Config('1s2 2*4', group="initial")
    fac.Config('1*1 2*6', group="transient")
    fac.Config('1s2 2*5', group="final")
    return "KLL-C"

def kll_n():
    """Electron config for KLL DR with n-like initial state"""
    fac.Config('1s2 2*5', group="initial")
    fac.Config('1*1 2*7', group="transient")
    fac.Config('1s2 2*6', group="final")
    return "KLL-N"

def kll_o():
    """Electron config for KLL DR with o-like initial state"""
    fac.Config('1s2 2*6', group="initial")
    fac.Config('1*1 2*8', group="transient")
    fac.Config('1s2 2*7', group="final")
    return "KLL-O"

###### KLM Settings
def klm_he():
    """Electron config for KLM DR with he-like initial state"""
    fac.Config('1s2 2*0 3*0', group="initial")
    fac.Config('1*1 2*1 3*1', group="transient")
    fac.Config('1s2 2*1 3*0', '1s2 2*0 3*1', group="final")
    return "KLM-He"

def klm_li():
    """Electron config for KLM DR with li-like initial state"""
    fac.Config('1s2 2*1 3*0', group="initial")
    fac.Config('1*1 2*2 3*1', group="transient")
    fac.Config('1s2 2*2 3*0', '1s2 2*1 3*1', group="final")
    return "KLM-Li"

def klm_be():
    """Electron config for KLM DR with be-like initial state"""
    fac.Config('1s2 2*2 3*0', group="initial")
    fac.Config('1*1 2*3 3*1', group="transient")
    fac.Config('1s2 2*3 3*0', '1s2 2*2 3*1', group="final")
    return "KLM-Be"

def klm_b():
    """Electron config for KLM DR with b-like initial state"""
    fac.Config('1s2 2*3 3*0', group="initial")
    fac.Config('1*1 2*4 3*1', group="transient")
    fac.Config('1s2 2*4 3*0', '1s2 2*3 3*1', group="final")
    return "KLM-B"

def klm_c():
    """Electron config for KLM DR with c-like initial state"""
    fac.Config('1s2 2*4 3*0', group="initial")
    fac.Config('1*1 2*5 3*1', group="transient")
    fac.Config('1s2 2*5 3*0', '1s2 2*4 3*1', group="final")
    return "KLM-C"

def klm_n():
    """Electron config for KLM DR with n-like initial state"""
    fac.Config('1s2 2*5 3*0', group="initial")
    fac.Config('1*1 2*6 3*1', group="transient")
    fac.Config('1s2 2*6 3*0', '1s2 2*5 3*1', group="final")
    return "KLM-N"

def klm_o():
    """Electron config for KLM DR with o-like initial state"""
    fac.Config('1s2 2*6 3*0', group="initial")
    fac.Config('1*1 2*7 3*1', group="transient")
    fac.Config('1s2 2*7 3*0', '1s2 2*6 3*1', group="final")
    return "KLM-O"