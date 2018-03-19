import facreader
import pandas as pd

# Set up script
AI_FILE = "data/K.o.ai"
TR_FILE = "data/K.o.tr"
OUT_FILE = "results/K.O.dr.txt"

# Read FAC Files
ai_header, ai_data = facreader.read_ai(AI_FILE)
tr_header, tr_data = facreader.read_tr(TR_FILE)


def total_tr(ILEV):
    """
    Method for computing total radiative decay rate for a certain state with FAC Identifier ILEV
    """
    filtered = tr_data.loc[tr_data['UPPER_ILEV'] == ILEV]
    return filtered["TR_RATE"].sum()

# Assemble DR Table
dr_data = ai_data[["BOUND_ILEV","FREE_ILEV", "DELTA_E", "AI_RATE", "DC_STRENGTH"]].copy()
# dr_data["TOTAL_TR_RATE"] = -1
# dr_data["RADIATIVE_FRACTION"] = -1
# dr_data["DR_CROSS_SECTION"] = -1
# Compute total rate of radiative decay for each bound state
dr_data.loc[:, "TOTAL_TR_RATE"] = dr_data.apply(lambda row: total_tr(row["BOUND_ILEV"]), axis=1)
# Compute the fraction of radiative and autoionising decay
dr_data.loc[:, "RADIATIVE_FRACTION"] = dr_data["TOTAL_TR_RATE"] / (dr_data["TOTAL_TR_RATE"] + dr_data["AI_RATE"])
# Compute the strength of the DR process decaying radiatively
dr_data.loc[:, "DR_CROSS_SECTION"] = dr_data["DC_STRENGTH"] * dr_data["RADIATIVE_FRACTION"]

# Save dr table to file
dr_data.to_csv(OUT_FILE, sep=" ", index=False)
print("Done!")