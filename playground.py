import factools.fileimport
import factools.reconstruction


# Set up script
AI_FILE = "example_data/K.b-kll.ai"
TR_FILE = "example_data/K.b-kll.tr"
LEV_FILE = "example_data/K.b-kll.lev"

# Read FAC Files
ai_header, ai_df = factools.fileimport.read_ai(AI_FILE)
tr_header, tr_df = factools.fileimport.read_tr(TR_FILE)
lev_header, lev_df = factools.fileimport.read_lev(LEV_FILE)

lev_df = factools.reconstruction.amend_level_dataframe(lev_df, verbose=True)
print(lev_df)