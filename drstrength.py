import facreader
import pandas as pd

ai_header, ai_data = facreader.read_ai("K.li.ai")
tr_header, tr_data = facreader.read_tr("K.li.tr")

def total_tr(ILEV):
    filtered = tr_data.loc[tr_data['UPPER_ILEV'] == ILEV]
    return filtered["TR_RATE"].sum()

dr_data = ai_data[["BOUND_ILEV","FREE_ILEV", "DELTA_E", "AI_RATE", "DC_STRENGTH"]]
dr_data["TOTAL_TR_RATE"] = dr_data.apply(lambda row: total_tr(row["BOUND_ILEV"]), axis=1)
dr_data["RADIATIVE_FRACTION"] = dr_data["TOTAL_TR_RATE"] / (dr_data["TOTAL_TR_RATE"] + dr_data["AI_RATE"])
dr_data["DR_CROSS_SECTION"] = dr_data["DC_STRENGTH"] * dr_data["RADIATIVE_FRACTION"]
print(dr_data)