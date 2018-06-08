import re
from itertools import chain, combinations

# MAX_NELE_N = {1:2, 2:8, 3:18, 4:32, 5:50, 6:72, 7:98, 8:128, 9:162, 10:200}
MAX_NELE_L = {"s":2, "p":6, "d":10, "f":14, "g":18, "h":22, "i":26, "k":30, "l":34, "m":38}
L_ORDER = ["s", "p", "d", "f", "g", "h", "i", "k", "l", "m"]

# Helper Method for creating powersets
def _powerset(iterable):
    """
    powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)
    https://stackoverflow.com/questions/18035595/powersets-in-python-using-itertools
    """
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def _parse_sname(sname):
    """
    Parse FAC's sname (non relativistic electron configuration) into a dict of dicts

    Example
    2s1 2p1 3s1 --> {2: {'s': 1, 'p': 1}, 3: {'s': 1}}
    """
    orb_nele = {}

    # split the string representing the non relativistic config into n and l levels
    for orbital in sname.split():
        orb = re.split(r"(\D)", orbital)
        n = int(orb[0])
        l = orb[1]
        nele = int(orb[2])
        if n not in orb_nele:
            orb_nele[n] = {}
        orb_nele[n][l] = nele
        # print(n, ":", l, ":", nele)
    print(sname, "-->", orb_nele)
    return orb_nele

def _parse_compl(compl):
    """
    Parse FAC's complex (number of electrons per n shell) into a dict

    Example
    1*2 2*2 3*7 --> {1: 2, 2: 2, 3: 7}
    """
    shell_nele = {}

    # split facs "complex" into numbers of electrons per n shell
    for shell in compl.split():
        she = re.split(r"\*", shell)
        n = int(she[0])
        nele = int(she[1])
        shell_nele[n] = nele
        # print(n, ":", nele)
    print(compl, "-->", shell_nele)
    return shell_nele

def _assemble_sname(orb_nele):
    ordered_orbitals = []
    ns = sorted(orb_nele.keys())
    for n in ns:
        ls = sorted(orb_nele[n].keys(), key=lambda l: L_ORDER.index(l))
        for l in ls:
            ordered_orbitals.append(str(n) + l + str(orb_nele[n][l]))
    return " ".join(ordered_orbitals)

def _reconstruct_full_sname(compl, sname):
    """
    This function tries to fill in the omitted parts of FAC's electron configurations
    sname (non relativistic electron configuration)
    """

    orb_nele = _parse_sname(sname)
    shell_nele = _parse_compl(compl)

    # Compute how many electrons are unaccounted for in each shell (exist in compl but not in sname)
    missing_nele = {}
    for n, nele in shell_nele.items():
        orb = orb_nele.get(n, {"def":0})
        sumele = sum(val for val in orb.values())
        missing_nele[n] = nele-sumele
    print("Missing Electrons -->", missing_nele)

    # try to figure out the omitted l symbols in each n shell
    omitted_orbitals = {}
    for n, missing in missing_nele.items():
        if missing > 0:
            # Figure out which orbitals (l) should be considered for this n shell
            consider = []
            for l in MAX_NELE_L:
                if MAX_NELE_L[l] <= missing: # If orbital has less electrons than are missing
                    if not (n in orb_nele and l in orb_nele[n]): # and it is not in sname
                        consider.append(l) # add it to the to be considered list
            print("Considered for shell:", n, "-->", consider)

            sol = []
            for cfg in _powerset(consider):
                sum_cfg = sum(MAX_NELE_L[l] for l in cfg)
                if sum_cfg == missing:
                    sol.append(cfg)

            if len(sol) == 0:
                print("No solution found for shell:", n)
            elif len(sol) > 1:
                print("More than one solution found for shell:", n, "--> Aborting")
                for s in sol:
                    print(s)
                raise ValueError("No unambiguous solution")
            elif len(sol) == 1:
                omitted_orbitals[n] = {l:MAX_NELE_L[l] for l in sol[0]}
                print("Determined omitted orbitals -->", omitted_orbitals[n])

    # Update the orbitals with the determined omissions
    for n in omitted_orbitals:
        if n in orb_nele:
            orb_nele[n].update(omitted_orbitals[n])
        else:
            orb_nele[n] = omitted_orbitals[n]
    print("Completed reconstruction -->", orb_nele)

    # Assemble name and return
    full_sname =  _assemble_sname(orb_nele)
    print("Generated full sname -->", full_sname)
    return full_sname

sname_memo = {}
def reconstruct_full_sname(compl, sname):
    """
    This function tries to fill in the omitted parts of FAC's electron configurations
    sname (non relativistic electron configuration)

    This function is a memoising wrapper around the actual routine
    """
    key = (compl, sname)
    if key not in sname_memo:
        sname_memo[key] = _reconstruct_full_sname(compl, sname)    
    return sname_memo[key]

def _reconstruct_full_name(sname, name):
    """
    This function tries to fill in the omitted parts of FAC's electron configurations
    name (relativistic electron configuration)
    """

    orb_nele = _parse_sname(sname)

    # # Compute how many electrons are unaccounted for in each shell (exist in compl but not in sname)
    # missing_nele = {}
    # for n, nele in shell_nele.items():
    #     orb = orb_nele.get(n, {"def":0})
    #     sumele = sum(val for val in orb.values())
    #     missing_nele[n] = nele-sumele
    # print("Missing Electrons -->", missing_nele)

    # # try to figure out the omitted l symbols in each n shell
    # omitted_orbitals = {}
    # for n, missing in missing_nele.items():
    #     if missing > 0:
    #         # Figure out which orbitals (l) should be considered for this n shell
    #         consider = []
    #         for l in MAX_NELE_L:
    #             if MAX_NELE_L[l] <= missing: # If orbital has less electrons than are missing
    #                 if not (n in orb_nele and l in orb_nele[n]): # and it is not in sname
    #                     consider.append(l) # add it to the to be considered list
    #         print("Considered for shell:", n, "-->", consider)

    #         sol = []
    #         for cfg in _powerset(consider):
    #             sum_cfg = sum(MAX_NELE_L[l] for l in cfg)
    #             if sum_cfg == missing:
    #                 sol.append(cfg)

    #         if len(sol) == 0:
    #             print("No solution found for shell:", n)
    #         elif len(sol) > 1:
    #             print("More than one solution found for shell:", n, "--> Aborting")
    #             for s in sol:
    #                 print(s)
    #             raise ValueError("No unambiguous solution")
    #         elif len(sol) == 1:
    #             omitted_orbitals[n] = {l:MAX_NELE_L[l] for l in sol[0]}
    #             print("Determined omitted orbitals -->", omitted_orbitals[n])

    # # Update the orbitals with the determined omissions
    # for n in omitted_orbitals:
    #     if n in orb_nele:
    #         orb_nele[n].update(omitted_orbitals[n])
    #     else:
    #         orb_nele[n] = omitted_orbitals[n]
    # print("Completed reconstruction -->", orb_nele)

    # # Assemble name and return
    # full_sname =  _assemble_sname(orb_nele)
    # print("Generated full sname -->", full_sname)
    # return full_sname

compl = "1*2 2*2 3*7"
sname = "2s1 2p1 3s1"
reconstruct_full_sname(compl, sname)