import facreader
import pandas as pd
import os

files = os.listdir("./data_complete_steffen")
filtered_files = []
for f in files:
    if ".ai" == f[-3:]:
        filtered_files.append(f)
print(filtered_files)
fails = []
successes = []
for fname in filtered_files:
    try:
        print(fname)
        # Set up script
        AI_FILE = "./data_complete_steffen/" + fname
        TR_FILE = "./data_complete_steffen/" + fname[:-3] + ".tr"
        OUT_FILE = "results_gs_batch/" + fname[:-3] + ".dr.txt"

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
        dr_data.loc[:, "DR_RECOMB_STRENGTH"] = dr_data["DC_STRENGTH"] * dr_data["RADIATIVE_FRACTION"]

        #Filter for transitions with ion initially in ground state
        dr_data = dr_data.loc[dr_data["FREE_ILEV"] == dr_data["FREE_ILEV"].min()]

        # Save dr table to file
        dr_data.to_csv(OUT_FILE, sep=" ", index=False)
        print("Done!")
        successes.append(fname)
    except:
        print("failed")
        fails.append(fname)
print("Successes")
print(successes)
print("Fails")
print(fails)
