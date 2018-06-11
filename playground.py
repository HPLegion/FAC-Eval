"""
for testing and playing around
"""

import factools.fileimport
import factools.reconstruction
import factools.dr


# Set up script
AI_FILE = "example_data/K.b-kll.ai"
TR_FILE = "example_data/K.b-kll.tr"
LEV_FILE = "example_data/K.b-kll.lev"

# Read FAC Files
ai_header, ai_df = factools.fileimport.read_ai(AI_FILE)
tr_header, tr_df = factools.fileimport.read_tr(TR_FILE)
lev_header, lev_df = factools.fileimport.read_lev(LEV_FILE)

# print(lev_df.head())
# print(tr_df.head())
# print(ai_df.head())

lev_df = factools.reconstruction.amend_level_dataframe(lev_df, verbose=False)

trans = factools.dr.dr_transition_table(lev_df, ai_df, tr_df, verbose=False)
recomb = factools.dr.dr_recombination_table(lev_df, ai_df, tr_df, verbose=False)
print(trans.head())
print(recomb)
