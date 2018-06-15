"""
Contains scripts for calculating DR relevant data with FAC

Can only be run in python 2.7 due to pfac
"""
import os
from pfac import fac

def run_for_all_elements():
    """
    Computes KLL and KLM for all Elements from Sodium(11) to Fermium (100)
    """
    elems = range(11, 101)

    kll_path = "./facoutput/KLL/"
    if not os.path.exists(kll_path):
        os.makedirs(kll_path)
    for z in elems:
        compute_kll(z, path=kll_path)

    klm_path = "./facoutput/KLM/"
    if not os.path.exists(klm_path):
        os.makedirs(klm_path)
    for z in elems:
        compute_klm(z, path=klm_path)


def compute_dr(z, dr_type, path=""):
    """
    Main routine, computes DR for given element and recombination process
    """
    elem = fac.ATOMICSYMBOL[z]
    # Initialise
    fac.Reinit()
    fac.SetAtom(elem)
    # Execute problem specific configuration
    type_name = dr_type()
    # Generate filenames
    f_stub = path + elem + "_" + type_name
    f_lev = f_stub + ".lev"
    f_lev_b = f_lev + ".b" # temp binary
    f_tr = f_stub + ".tr"
    f_tr_b = f_tr + ".b" # temp binary
    f_ai = f_stub + ".ai"
    f_ai_b = f_ai + ".b" # temp binary
    # Start solving
    fac.ConfigEnergy(0)
    # According to the manual we should Optimize on the recombined ion
    # (have seen other things out in the wild)
    fac.OptimizeRadial(["final"])
    fac.ConfigEnergy(1)
    # Compute structure and energy levels
    fac.Structure(f_lev_b, ["initial", "transient", "final"])
    fac.MemENTable(f_lev_b)
    fac.PrintTable(f_lev_b, f_lev, 1)
    # Compute the transisiton table for radiative decay
    # Transition Table defaults to m=0 since FAC1.0.7 (not in current docs)
    # which computes all multipoles according to new (unreleased) docs
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
    """
    Convenience function for automatically computing all KLL-like transitions
    """
    print("Starting KLL calculations for " + fac.ATOMICSYMBOL[z] + "...")
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
    """
    Convenience function for automatically computing all KLM-like transitions
    """
    print("Starting KLM calculations for " + fac.ATOMICSYMBOL[z] + "...")
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
    if z > 9:
        compute_dr(z, klm_f, path)

def compute_lmm(z, path=""):
    """
    Convenience function for automatically computing all LMM-like transitions
    """
    print("Starting LMM calculations for " + fac.ATOMICSYMBOL[z] + "...")
    if z > 3:
        compute_dr(z, lmm_li, path)
    if z > 4:
        compute_dr(z, lmm_be, path)
    if z > 5:
        compute_dr(z, lmm_b, path)
    if z > 6:
        compute_dr(z, lmm_c, path)
    if z > 7:
        compute_dr(z, lmm_n, path)
    if z > 8:
        compute_dr(z, lmm_o, path)
    if z > 9:
        compute_dr(z, lmm_f, path)
    if z > 10:
        compute_dr(z, lmm_ne, path)
    if z > 11:
        compute_dr(z, lmm_na, path)
    if z > 12:
        compute_dr(z, lmm_mg, path)
    if z > 13:
        compute_dr(z, lmm_al, path)
    if z > 14:
        compute_dr(z, lmm_si, path)
    if z > 15:
        compute_dr(z, lmm_p, path)
    if z > 16:
        compute_dr(z, lmm_s, path)
    if z > 17:
        compute_dr(z, lmm_cl, path)
    if z > 18:
        compute_dr(z, lmm_ar, path)
    if z > 19:
        compute_dr(z, lmm_k, path)
    if z > 20:
        compute_dr(z, lmm_ca, path)
    if z > 21:
        compute_dr(z, lmm_sc, path)
    if z > 22:
        compute_dr(z, lmm_ti, path)
    if z > 23:
        compute_dr(z, lmm_v, path)
    if z > 24:
        compute_dr(z, lmm_cr, path)
    if z > 25:
        compute_dr(z, lmm_mn, path)
    if z > 26:
        compute_dr(z, lmm_fe, path)
    if z > 27:
        compute_dr(z, lmm_co, path)
    if z > 28:
        compute_dr(z, lmm_ni, path)

###### KLL Settings
def kll_he():
    """Electron config for KLL DR with he-like initial state"""
    fac.Config('1*2 2*0', group="initial")
    fac.Config('1*1 2*2', group="transient")
    fac.Config('1*2 2*1', group="final")
    return "KLL-He"

def kll_li():
    """Electron config for KLL DR with li-like initial state"""
    fac.Config('1*2 2*1', group="initial")
    fac.Config('1*1 2*3', group="transient")
    fac.Config('1*2 2*2', group="final")
    return "KLL-Li"

def kll_be():
    """Electron config for KLL DR with be-like initial state"""
    fac.Config('1*2 2*2', group="initial")
    fac.Config('1*1 2*4', group="transient")
    fac.Config('1*2 2*3', group="final")
    return "KLL-Be"

def kll_b():
    """Electron config for KLL DR with b-like initial state"""
    fac.Config('1*2 2*3', group="initial")
    fac.Config('1*1 2*5', group="transient")
    fac.Config('1*2 2*4', group="final")
    return "KLL-B"

def kll_c():
    """Electron config for KLL DR with c-like initial state"""
    fac.Config('1*2 2*4', group="initial")
    fac.Config('1*1 2*6', group="transient")
    fac.Config('1*2 2*5', group="final")
    return "KLL-C"

def kll_n():
    """Electron config for KLL DR with n-like initial state"""
    fac.Config('1*2 2*5', group="initial")
    fac.Config('1*1 2*7', group="transient")
    fac.Config('1*2 2*6', group="final")
    return "KLL-N"

def kll_o():
    """Electron config for KLL DR with o-like initial state"""
    fac.Config('1*2 2*6', group="initial")
    fac.Config('1*1 2*8', group="transient")
    fac.Config('1*2 2*7', group="final")
    return "KLL-O"

###### KLM Settings
# def klm_he():
#     """Electron config for KLM DR with he-like initial state"""
#     fac.Config('1*2 2*0 3*0', group="initial")
#     fac.Config('1*1 2*1 3*1', group="transient")
#     fac.Config('1*2 2*1 3*0', '1*2 2*0 3*1', group="final")
#     return "KLM-He"

# def klm_li():
#     """Electron config for KLM DR with li-like initial state"""
#     fac.Config('1*2 2*1 3*0', group="initial")
#     fac.Config('1*1 2*2 3*1', group="transient")
#     fac.Config('1*2 2*2 3*0', '1*2 2*1 3*1', group="final")
#     return "KLM-Li"

# def klm_be():
#     """Electron config for KLM DR with be-like initial state"""
#     fac.Config('1*2 2*2 3*0', group="initial")
#     fac.Config('1*1 2*3 3*1', group="transient")
#     fac.Config('1*2 2*3 3*0', '1*2 2*2 3*1', group="final")
#     return "KLM-Be"

# def klm_b():
#     """Electron config for KLM DR with b-like initial state"""
#     fac.Config('1*2 2*3 3*0', group="initial")
#     fac.Config('1*1 2*4 3*1', group="transient")
#     fac.Config('1*2 2*4 3*0', '1*2 2*3 3*1', group="final")
#     return "KLM-B"

# def klm_c():
#     """Electron config for KLM DR with c-like initial state"""
#     fac.Config('1*2 2*4 3*0', group="initial")
#     fac.Config('1*1 2*5 3*1', group="transient")
#     fac.Config('1*2 2*5 3*0', '1*2 2*4 3*1', group="final")
#     return "KLM-C"

# def klm_n():
#     """Electron config for KLM DR with n-like initial state"""
#     fac.Config('1*2 2*5 3*0', group="initial")
#     fac.Config('1*1 2*6 3*1', group="transient")
#     fac.Config('1*2 2*6 3*0', '1*2 2*5 3*1', group="final")
#     return "KLM-N"

# def klm_o():
#     """Electron config for KLM DR with o-like initial state"""
#     fac.Config('1*2 2*6 3*0', group="initial")
#     fac.Config('1*1 2*7 3*1', group="transient")
#     fac.Config('1*2 2*7 3*0', '1*2 2*6 3*1', group="final")
#     return "KLM-O"

# def klm_f():
#     """Electron config for KLM DR with f-like initial state"""
#     fac.Config('1*2 2*7 3*0', group="initial")
#     fac.Config('1*1 2*8 3*1', group="transient")
#     fac.Config('1*2 2*8 3*0', '1*2 2*7 3*1', group="final")
#     return "KLM-O"

def klm_he():
    """Electron config for KLM DR with he-like initial state"""
    fac.Config('1*2 2*0 3*0', group="initial")
    fac.Config('1*1 2*1 3*1', group="transient")
    fac.Config('1*2 2*1 3*0', '1*2 2*0 3*1', '1*1 2*2 3*0', group="final")
    return "KLM-He"

def klm_li():
    """Electron config for KLM DR with li-like initial state"""
    fac.Config('1*2 2*1 3*0', group="initial")
    fac.Config('1*1 2*2 3*1', group="transient")
    fac.Config('1*2 2*2 3*0', '1*2 2*1 3*1', '1*1 2*3 3*0', group="final")
    return "KLM-Li"

def klm_be():
    """Electron config for KLM DR with be-like initial state"""
    fac.Config('1*2 2*2 3*0', group="initial")
    fac.Config('1*1 2*3 3*1', group="transient")
    fac.Config('1*2 2*3 3*0', '1*2 2*2 3*1', '1*1 2*4 3*0', group="final")
    return "KLM-Be"

def klm_b():
    """Electron config for KLM DR with b-like initial state"""
    fac.Config('1*2 2*3 3*0', group="initial")
    fac.Config('1*1 2*4 3*1', group="transient")
    fac.Config('1*2 2*4 3*0', '1*2 2*3 3*1', '1*1 2*5 3*0', group="final")
    return "KLM-B"

def klm_c():
    """Electron config for KLM DR with c-like initial state"""
    fac.Config('1*2 2*4 3*0', group="initial")
    fac.Config('1*1 2*5 3*1', group="transient")
    fac.Config('1*2 2*5 3*0', '1*2 2*4 3*1', '1*1 2*6 3*0', group="final")
    return "KLM-C"

def klm_n():
    """Electron config for KLM DR with n-like initial state"""
    fac.Config('1*2 2*5 3*0', group="initial")
    fac.Config('1*1 2*6 3*1', group="transient")
    fac.Config('1*2 2*6 3*0', '1*2 2*5 3*1', '1*1 2*7 3*0', group="final")
    return "KLM-N"

def klm_o():
    """Electron config for KLM DR with o-like initial state"""
    fac.Config('1*2 2*6 3*0', group="initial")
    fac.Config('1*1 2*7 3*1', group="transient")
    fac.Config('1*2 2*7 3*0', '1*2 2*6 3*1', '1*1 2*8 3*0', group="final")
    return "KLM-O"

def klm_f():
    """Electron config for KLM DR with f-like initial state"""
    fac.Config('1*2 2*7 3*0', group="initial")
    fac.Config('1*1 2*8 3*1', group="transient")
    fac.Config('1*2 2*8 3*0', '1*2 2*7 3*1', group="final")
    return "KLM-O"

###### LMM Settings
def lmm_li():
    """Electron config for LMM DR with li-like initial state"""
    fac.Closed('1s')
    fac.Config('2s1', group="initial")
    fac.Config('2*0 3*2', group="transient")
    fac.Config('2*1 3*1', group="final")
    return "LMM-Li"

def lmm_be():
    """Electron config for LMM DR with be-like initial state"""
    fac.Closed('1s')
    fac.Config('2s2', group="initial")
    fac.Config('2*1 3*2', group="transient")
    fac.Config('2*2 3*1', group="final")
    return "LMM-Be"

def lmm_b():
    """Electron config for LMM DR with b-like initial state"""
    fac.Closed('1s')
    fac.Config('2s2 2p1', group="initial")
    fac.Config('2*2 3*2', group="transient")
    fac.Config('2*3 3*1', group="final")
    return "LMM-B"

def lmm_c():
    """Electron config for LMM DR with c-like initial state"""
    fac.Closed('1s')
    fac.Config('2s2 2p2', group="initial")
    fac.Config('2*3 3*2', group="transient")
    fac.Config('2*4 3*1', group="final")
    return "LMM-C"

def lmm_n():
    """Electron config for LMM DR with n-like initial state"""
    fac.Closed('1s')
    fac.Config('2s2 2p3', group="initial")
    fac.Config('2*4 3*2', group="transient")
    fac.Config('2*5 3*1', group="final")
    return "LMM-N"
    
def lmm_o():
    """Electron config for LMM DR with o-like initial state"""
    fac.Closed('1s')
    fac.Config('2s2 2p4', group="initial")
    fac.Config('2*5 3*2', group="transient")
    fac.Config('2*6 3*1', group="final")
    return "LMM-O"

def lmm_f():
    """Electron config for LMM DR with f-like initial state"""
    fac.Closed('1s')
    fac.Config('2s2 2p5', group="initial")
    fac.Config('2*6 3*2', group="transient")
    fac.Config('2*7 3*1', group="final")
    return "LMM-F"

def lmm_ne():
    """Electron config for LMM DR with ne-like initial state"""
    fac.Closed('1s')
    fac.Config('2s2 2p6', group="initial")
    fac.Config('2*7 3*2', group="transient")
    fac.Config('2*8 3*1', group="final")
    return "LMM-Ne"

def lmm_na():
    """Electron config for LMM DR with na-like initial state"""
    fac.Closed('1s')
    fac.Config('2*8 3s1', group="initial")
    fac.Config('2*7 3*3', group="transient")
    fac.Config('2*8 3*2', group="final")
    return "LMM-Na"

def lmm_mg():
    """Electron config for LMM DR with mg-like initial state"""
    fac.Closed('1s')
    fac.Config('2*8 3s2', group="initial")
    fac.Config('2*7 3*4', group="transient")
    fac.Config('2*8 3*3', group="final")
    return "LMM-Mg"

def lmm_al():
    """Electron config for LMM DR with al-like initial state"""
    fac.Closed('1s')
    fac.Config('2*8 3s2 3p1', group="initial")
    fac.Config('2*7 3*5', group="transient")
    fac.Config('2*8 3*4', group="final")
    return "LMM-Al"

def lmm_si():
    """Electron config for LMM DR with si-like initial state"""
    fac.Closed('1s')
    fac.Config('2*8 3s2 3p2', group="initial")
    fac.Config('2*7 3*6', group="transient")
    fac.Config('2*8 3*5', group="final")
    return "LMM-Si"

def lmm_p():
    """Electron config for LMM DR with p-like initial state"""
    fac.Closed('1s')
    fac.Config('2*8 3s2 3p3', group="initial")
    fac.Config('2*7 3*7', group="transient")
    fac.Config('2*8 3*6', group="final")
    return "LMM-P"

def lmm_s():
    """Electron config for LMM DR with s-like initial state"""
    fac.Closed('1s')
    fac.Config('2*8 3s2 3p4', group="initial")
    fac.Config('2*7 3*8', group="transient")
    fac.Config('2*8 3*7', group="final")
    return "LMM-S"

def lmm_cl():
    """Electron config for LMM DR with cl-like initial state"""
    fac.Closed('1s')
    fac.Config('2*8 3s2 3p5', group="initial")
    fac.Config('2*7 3*9', group="transient")
    fac.Config('2*8 3*8', group="final")
    return "LMM-Cl"

def lmm_ar():
    """Electron config for LMM DR with ar-like initial state"""
    fac.Closed('1s')
    fac.Config('2*8 3s2 3p6', group="initial")
    fac.Config('2*7 3*10', group="transient")
    fac.Config('2*8 3*9', group="final")
    return "LMM-Cl"

def lmm_k():
    """Electron config for LMM DR with k-like initial state"""
    fac.Closed('1s')
    fac.Config('2*8 3s2 3p6 4s1', group="initial")
    fac.Config('2*7 3*10 4s1', group="transient")
    fac.Config('2*8 3*9 4s1', group="final")
    return "LMM-K"

def lmm_ca():
    """Electron config for LMM DR with ca-like initial state"""
    fac.Closed('1s 4s')
    fac.Config('2*8 3s2 3p6', group="initial")
    fac.Config('2*7 3*10', group="transient")
    fac.Config('2*8 3*9', group="final")
    return "LMM-Ca"

def lmm_sc():
    """Electron config for LMM DR with sc-like initial state"""
    fac.Closed('1s 4s')
    fac.Config('2*8 3s2 3p6 3d1', group="initial")
    fac.Config('2*7 3*11', group="transient")
    fac.Config('2*8 3*10', group="final")
    return "LMM-Sc"

def lmm_ti():
    """Electron config for LMM DR with ti-like initial state"""
    fac.Closed('1s 4s')
    fac.Config('2*8 3s2 3p6 3d2', group="initial")
    fac.Config('2*7 3*12', group="transient")
    fac.Config('2*8 3*11', group="final")
    return "LMM-Ti"

def lmm_v():
    """Electron config for LMM DR with v-like initial state"""
    fac.Closed('1s 4s')
    fac.Config('2*8 3s2 3p6 3d3', group="initial")
    fac.Config('2*7 3*13', group="transient")
    fac.Config('2*8 3*12', group="final")
    return "LMM-V"

def lmm_cr():
    """Electron config for LMM DR with cr-like initial state"""
    fac.Closed('1s 4s')
    fac.Config('2*8 3s2 3p6 3d4', group="initial")
    fac.Config('2*7 3*14', group="transient")
    fac.Config('2*8 3*13', group="final")
    return "LMM-Cr"

def lmm_mn():
    """Electron config for LMM DR with mn-like initial state"""
    fac.Closed('1s 4s')
    fac.Config('2*8 3s2 3p6 3d5', group="initial")
    fac.Config('2*7 3*15', group="transient")
    fac.Config('2*8 3*14', group="final")
    return "LMM-Mn"

def lmm_fe():
    """Electron config for LMM DR with fe-like initial state"""
    fac.Closed('1s 4s')
    fac.Config('2*8 3s2 3p6 3d6', group="initial")
    fac.Config('2*7 3*16', group="transient")
    fac.Config('2*8 3*15', group="final")
    return "LMM-Fe"

def lmm_co():
    """Electron config for LMM DR with co-like initial state"""
    fac.Closed('1s 4s')
    fac.Config('2*8 3s2 3p6 3d7', group="initial")
    fac.Config('2*7 3*17', group="transient")
    fac.Config('2*8 3*16', group="final")
    return "LMM-Co"

def lmm_ni():
    """Electron config for LMM DR with ni-like initial state"""
    fac.Closed('1s 4s')
    fac.Config('2*8 3s2 3p6 3d8', group="initial")
    fac.Config('2*7 3*18', group="transient")
    fac.Config('2*8 3*17', group="final")
    return "LMM-Ci"