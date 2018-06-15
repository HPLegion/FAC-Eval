"""
for testing and playing around
"""

import factools.fileimport
import factools.reconstruction
import factools.dr


# Set up script
AI_FILE = "cs/Cs_LMM-Li.ai"
TR_FILE = "cs/Cs_LMM-Li.tr"
LEV_FILE = "cs/Cs_LMM-Li.lev"

# Read FAC Files
ai_header, ai_df = factools.fileimport.read_ai(AI_FILE)
tr_header, tr_df = factools.fileimport.read_tr(TR_FILE)
lev_header, lev_df = factools.fileimport.read_lev(LEV_FILE)

# print(lev_df.head())
# print(tr_df.head())
# print(ai_df.head())

lev_df = factools.reconstruction.amend_level_dataframe(lev_df, verbose=True)

trans = factools.dr.dr_transition_table(lev_df, ai_df, tr_df, verbose=True)
recomb = factools.dr.dr_recombination_table(lev_df, ai_df, tr_df, verbose=True)
print(trans.head())
print(recomb)
