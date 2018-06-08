"""
Contains Methods for extracting DR related data from FAC Results
"""

import pandas as pd

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
DR_RECOMB_STRENGTH = "DR_RECOMB_STRENGTH"
RECOMB_TYPE = "RECOMB_TYPE"


def recomb_type(inital_name, transient_name):
    """
    Given an intital and transient FAC electron config (name) computes the kind of Transition
    i.e. DR, TR, QR,...
    """
    return "not impl"



def dr_table(lev_df, ai_df, tr_df, filter_gs=True):
    """
    Assembles a detailed table of (di) electronic recombinations based on the FAC files

    filter_gs - filter table  to contain only transitions starting in the ground state
    """

    def get_name(ilev):
        """ grabs the sname for ilev from the level dataframe """
        row_ind = lev_df.index[lev_df["ILEV"] == ilev].tolist()[0]
        return lev_df.at[row_ind, "FULL_NAME"]

    COL_ORDER = [INIT_ILEV, INIT_NAME, TRANS_ILEV, TRANS_NAME, FINAL_ILEV, FINAL_NAME,
                 RECOMB_TYPE, DR_RECOMB_STRENGTH, DE_AI, AI_RATE, DC_STRENGTH,
                 DE_TR, TR_RATE]

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
        dr_row[RECOMB_TYPE] = recomb_type(dr_row[INIT_NAME], dr_row[TRANS_NAME])

        # Go thorugh all realted radiative decays
        filtered_tr = tr_df.loc[tr_df[UPPER_ILEV] == dr_row[TRANS_ILEV]]
        for (_, tr_row) in filtered_tr.iterrows():
            # Load Final state ID and sname
            dr_row[FINAL_ILEV] = tr_row[LOWER_ILEV]
            dr_row[FINAL_NAME] = get_name(dr_row[FINAL_ILEV])
            # Load TR Data
            dr_row[DE_TR] = tr_row[DE]
            dr_row[TR_RATE] = tr_row[TR_RATE]
            # Compute recomb strength
            dr_row[DR_RECOMB_STRENGTH] = dr_row[TR_RATE] / (dr_row[TR_RATE] + dr_row[AI_RATE])
            dr_tab.append(dr_row.copy())
            print(dr_row[INIT_NAME], "\n-->", dr_row[TRANS_NAME], "\n-->", dr_row[FINAL_NAME])
            
    dr_tab = pd.DataFrame(dr_tab)
    dr_tab = dr_tab[COL_ORDER]
    dr_tab.sort_values([DE_AI, DE_TR], inplace=True)
    return dr_tab
