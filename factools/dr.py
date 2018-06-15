"""
Contains Methods for extracting DR related data from FAC Results
"""

import pandas as pd
from factools.reconstruction import parse_name

INIT_ILEV = "INITAL_ILEV"
TRANS_ILEV = "TRANSIENT_ILEV"
FINAL_ILEV = "FINAL_ILEV"
FREE_ILEV = "FREE_ILEV"
BOUND_ILEV = "BOUND_ILEV"
UPPER_ILEV = "UPPER_ILEV"
LOWER_ILEV = "LOWER_ILEV"
INIT_NAME = "INITAL_NAME"
TRANS_NAME = "TRANSIENT_NAME"
FINAL_NAME = "FINAL_NAME"
DE_AI = "DELTA_E_AI"
DE_TR = "DELTA_E_TR"
DE = "DELTA_E"
AI_RATE = "AI_RATE"
TR_RATE = "TR_RATE"
DC_STRENGTH = "DC_STRENGTH"
RECOMB_STRENGTH = "RECOMB_STRENGTH"
TRANSITION_STRENGTH = "TRANSITION_STRENGTH"
RECOMB_TYPE = "RECOMB_TYPE"
RECOMB_NAME = "RECOMB_NAME"

RECOMB_TYPES = {2:"DR", 3:"TR", 4:"QR"}
SHELL_NAMES = {1:"K", 2:"L", 3:"M", 4:"N", 5:"O", 6:"P", 7:"Q", 8:"R"}

def recomb_info(inital_name, transient_name):
    """
    Given an intital and transient FAC electron config (name) computes the kind of Transition
    i.e. DR, TR, QR,... and KLL KLM KLLLL KLLMM etc.
    """
    (initial, _) = parse_name(inital_name)
    (transient, _) = parse_name(transient_name)
    diff = 0
    shell_lost = []
    shell_gained = []
    ns = initial.keys() | transient.keys()
    for n in ns: #Loop over all shells
        ini_shell = initial.get(n, {})
        tra_shell = transient.get(n, {})
        lpms = ini_shell.keys() | tra_shell.keys()
        for lpm in lpms: # and over all orbitals in each shell
            d = tra_shell.get(lpm, 0) - ini_shell.get(lpm, 0)
            diff += abs(d) # count changes in configuration
            for _ in range(abs(d)):
                if d < 0: # and reconstruct the "name" e.g.KLL etc.
                    shell_lost.append(SHELL_NAMES[n])
                else:
                    shell_gained.append(SHELL_NAMES[n])

    re_name = "".join(sorted(shell_lost)) + "-" + "".join(sorted(shell_gained))

    diff = int((diff + 1) / 2)
    if diff in RECOMB_TYPES:
        re_type = RECOMB_TYPES[diff]
    else:
        re_type = str(diff) + "R"

    return (re_type, re_name)

def dr_recombination_table(lev_df, ai_df, tr_df, filter_gs=True, verbose=False):
    """
    Assembles a condensed table of di(multi)electronic recombinations
    where all optical transition information is omitted and purely the recombination matters
    I.e. electron energy, total recombination strength, recom type.
    """
    COL_ORDER = [DE_AI, RECOMB_STRENGTH, RECOMB_TYPE, RECOMB_NAME]
    df = dr_transition_table(lev_df, ai_df, tr_df, filter_gs, verbose)
    grp = df.groupby([INIT_ILEV, TRANS_ILEV, RECOMB_TYPE, RECOMB_NAME], as_index=False)

    recomb = grp.agg({TRANSITION_STRENGTH:"sum", DE_AI:"mean"})
    recomb.rename(columns={TRANSITION_STRENGTH:RECOMB_STRENGTH}, inplace=True)
    recomb.drop([INIT_ILEV, TRANS_ILEV], axis=1, inplace=True)
    recomb.sort_values(DE_AI, inplace=True)
    recomb.reset_index(drop=True, inplace=True)
    recomb = recomb[COL_ORDER]
    return recomb


def dr_transition_table(lev_df, ai_df, tr_df, filter_gs=True, verbose=False):
    """
    Assembles a detailed table of (di) electronic recombinations based on the FAC files

    filter_gs - filter table  to contain only transitions starting in the ground state
    """

    def get_name(ilev):
        """ grabs the sname for ilev from the level dataframe """
        row_ind = lev_df.index[lev_df["ILEV"] == ilev].tolist()[0]
        return lev_df.at[row_ind, "FULL_NAME"]

    COL_ORDER = [INIT_ILEV, INIT_NAME, TRANS_ILEV, TRANS_NAME, FINAL_ILEV, FINAL_NAME, RECOMB_TYPE,
                 RECOMB_NAME, DE_AI, AI_RATE, DC_STRENGTH, DE_TR, TR_RATE, TRANSITION_STRENGTH]

    if filter_gs:
        ai_df = ai_df.loc[ai_df[FREE_ILEV] == ai_df[FREE_ILEV].min()]

    dr_tab = []
    for (_, ai_row) in ai_df.iterrows():
        dr_row = {}
        # Load Level IDs and snames
        dr_row[INIT_ILEV] = ai_row[FREE_ILEV]
        dr_row[TRANS_ILEV] = ai_row[BOUND_ILEV]
        dr_row[INIT_NAME] = get_name(dr_row[INIT_ILEV])
        dr_row[TRANS_NAME] = get_name(dr_row[TRANS_ILEV])
        # Load AI Data
        dr_row[DE_AI] = ai_row[DE]
        dr_row[AI_RATE] = ai_row[AI_RATE]
        dr_row[DC_STRENGTH] = ai_row[DC_STRENGTH]
        re_type, re_name = recomb_info(dr_row[INIT_NAME], dr_row[TRANS_NAME])
        dr_row[RECOMB_TYPE] = re_type
        dr_row[RECOMB_NAME] = re_name
        # Go thorugh all related radiative decays
        filtered_tr = tr_df.loc[tr_df[UPPER_ILEV] == dr_row[TRANS_ILEV]]
        total_tr_rate = filtered_tr["TR_RATE"].sum()
        for (_, tr_row) in filtered_tr.iterrows():
            # Load Final state ID and sname
            dr_row[FINAL_ILEV] = int(tr_row[LOWER_ILEV])
            dr_row[FINAL_NAME] = get_name(dr_row[FINAL_ILEV])
            # Load TR Data
            dr_row[DE_TR] = tr_row[DE]
            dr_row[TR_RATE] = tr_row[TR_RATE]
            # Compute recomb strength
            rad_frac = dr_row[TR_RATE] / (total_tr_rate + dr_row[AI_RATE])
            dr_row[TRANSITION_STRENGTH] = rad_frac * dr_row[DC_STRENGTH]
            dr_tab.append(dr_row.copy())
            if verbose:
                print(dr_row[RECOMB_TYPE], "---", dr_row[RECOMB_NAME],
                      "\n", dr_row[INIT_NAME],
                      "\n-->", dr_row[TRANS_NAME],
                      "\n-->", dr_row[FINAL_NAME],
                      "\n--------------------------------------------")

    dr_tab = pd.DataFrame(dr_tab)
    dr_tab = dr_tab[COL_ORDER]
    dr_tab.sort_values([DE_AI, DE_TR], inplace=True)
    dr_tab.reset_index(drop=True, inplace=True)
    return dr_tab
