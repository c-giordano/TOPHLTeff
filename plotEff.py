#!/usr/bin/env python3
import os
import shutil
import argparse
import ROOT
import plotHelper as ph
import usefulFunc as uf

parser = argparse.ArgumentParser(description="Overlay HLT efficiencies")
parser.add_argument("--user",type=str, default=os.environ.get("USER", ""),help="EOS username to build base paths")
parser.add_argument("--version", type=str, default="v1", help="Output version name (e.g. v1, v2)")
# hadronic / muon / electron
parser.add_argument("--hlt", choices=["hadronic", "muon", "electron"], required=True, help="HLT families hadronic, muon or electron")
parser.add_argument("--eras", nargs="+", help="List of eras for normal overlay")
parser.add_argument("--include-2024", action="store_true", help="If set, append 2024I ")
# special case
parser.add_argument("--special", action="store_true", help="Compare pre/post digi-morphing for a single era")
parser.add_argument("--specialEra",type=str, default="2025G", help="Era used for digi comparison (default: 2025G), ignored if --special is not set")
parser.add_argument("--inputDir", type=str, default=None, help="(es. v5ForMuon2025_10)")

args = parser.parse_args()

if args.user == ['cgiordan']: user_dir = 'c/cgiordan'
elif args.user == ['easilar']: user_dir = 'e/easilar'

# variables dictionary
triggerVarMap = {
    "HLTAll":      ["HT", "jet_6pt", "nb"],
    "HLTAll_2b":   ["nb", "jet_6pt", "HT"],
    "HLTAll_1b":   ["nb", "jet_6pt", "HT"],
    "HLTAll_3b":   ["nb", "jet_6pt", "HT"],
    "HLTAll_4b":   ["nb", "jet_6pt", "HT"],
    "HH":          ["HT", "jet_6pt", "nb"],
    "HLTcrossEle": ["ele_1pt", "ele_1eta", "HT"],
    "HLTbothEle":  ["ele_1pt", "ele_1eta", "HT"],
    "HLTsingleEle":["ele_1pt", "ele_1eta", "HT"],
    "HLTcrossMu":  ["muon_1pt", "muon_1eta", "HT"],
    "HLTbothMu":   ["muon_1pt", "muon_1eta", "HT"],
    "HLTsingleMu": ["muon_1pt", "muon_1eta", "HT"],
}

# set of triggers
HLT_BY_FAMILY = {
    "hadronic":     [ "HLTAll", "HH", "HLTAll_1b", "HLTAll_2b", "HLTAll_3b", "HLTAll_4b"],
    "muon":         [ "HLTcrossMu", "HLTbothMu", "HLTsingleMu" ],
    "electron":     [ "HLTcrossEle", "HLTbothEle", "HLTsingleEle" ],
}


def build_eff_path(hlt_family, era, stage=None):
    """
    Path to eff.root file
    """
    base_dir = os.path.join("/eos/user", args.user[0], args.user, "forTopHLT")

    campaign_dir = args.inputDir
    if campaign_dir is None:
        raise RuntimeError("--inputDir is required to build the path (e.g. v5ForMuon2025_10)")

    # 2025X
    if era.startswith("2025"):
        if hlt_family == "hadronic":
            tag_base = "v5Hadronic_{}".format(era)
        elif hlt_family == "muon":
            tag_base = "v5Muon_{}".format(era)
        elif hlt_family == "electron":
            tag_base = "v5Electron_{}".format(era)
        else:
            raise ValueError("Unknown HLT family: {}".format(hlt_family))

        if stage is None:
            tag = tag_base
        elif stage == "preDigi":
            tag = "{}_preDigi".format(tag_base)
        elif stage == "postDigi":
            tag = "{}_postDigi".format(tag_base)
        else:
            raise ValueError("Unknown stage: {}".format(stage))

        return "{}/{}/{}/result/{}/eff.root".format(base_dir, era, campaign_dir, tag)

    # 2024I
    if era == "2024I":
        if hlt_family == "hadronic":
            campaign = "v1ForHadronic2024"; tag = "v2ttHPhaseSpace_2024I"
        elif hlt_family == "muon":
            campaign = "v1ForMuon2024I";    tag = "v5Muon_2024I"
        elif hlt_family == "electron":
            campaign = "v1ForEle2024I";     tag = "v1ttAndHT200_2024I"
        else:
            raise ValueError("Unknown HLT family: {}".format(hlt_family))
        return "{}/{}/{}/result/{}/eff.root".format(base_dir, era, campaign, tag)

    raise ValueError("Unsupported era: {}".format(era))



def getOutDir(isHadronic, HLT, version):
    base_dir = os.path.join("/eos/user", args.user[0], args.user, "www/forTopHLT")
    subdir = "Hadronic" if isHadronic else "Leptonic"
    out_dir = os.path.join(base_dir, subdir, HLT, version)

    if not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)
    return out_dir + "/"

def copy_index_file(outDir):
    """
    Copy index.php from www tooutput directory
    """
    src_index = "/eos/user/c/cgiordan/www/index.php"
    dst_index = os.path.join(outDir, "index.php")

    if not os.path.exists(src_index):
        print(f"WARNING: Source index.php not found at {src_index}")
        return

    try:
        shutil.copyfile(src_index, dst_index)
        print(f"Copied index.php to {dst_index}")
    except Exception as e:
        print(f"Failed to copy index.php: {e}")



def effVsEras(inputList, HLT, legendList, isHadronic, version):
    """
    Draw eff.root (inputList) for all the triggerVarMap[HLT]
    """
    outDir = getOutDir(isHadronic, HLT, version)
    copy_index_file(outDir)

    var_list = triggerVarMap[HLT]

    for var in var_list:
        effList = []
        eraList = []

        for eff_file in inputList:
            eff = ph.getEffFromFile(eff_file, [f"de_{var}_{HLT}", f"nu_{var}_{HLT}"])
            era = uf.extract_era_from_path(eff_file)
            effList.append(eff)
            eraList.append(era)

        if not effList:
            print(f"No efficiency file found for var={var}, HLT={HLT}")
            continue

        xmin = effList[0].GetTotalHistogram().GetXaxis().GetXmin()
        xmax = effList[0].GetTotalHistogram().GetXaxis().GetXmax()

        plotName = f"{outDir}HLTEff_{var}_{HLT}.png"

        this_legend = legendList if legendList is not None else eraList

        ph.plotOverlay(
            effList,
            this_legend,
            "L1T+HLT efficiency",
            plotName,
            xmin,
            xmax,
            eraList,      # usi le ere come “label tecnica” per colori/stili
            [0, 1.1]
        )


# =======================
#   MAIN
# =======================

def main():
    isHadronic = (args.hlt == "hadronic")

    if args.special:
        era = args.specialEra
        effList = [
            build_eff_path(args.hlt, era, stage="preDigi"),
            build_eff_path(args.hlt, era, stage="postDigi"),
        ]
        legendList = [
            f"{era} (pre digi-morphing)",
            f"{era} (post digi-morphing)",
        ]
        eras_info = [era]

    else:
        # standard: multiple eras overlay
        if args.eras:
            eras = args.eras
        else:
            # default ragionevole
            eras = ["2025C", "2025D", "2025E", "2025F", "2025G"]

        if args.include_2024 and "2024I" not in eras:
            eras.append("2024I")

        effList = [build_eff_path(args.hlt, era) for era in eras]
        legendList = eras[:]  # copia
        eras_info = eras

    hlt_list = HLT_BY_FAMILY[args.hlt]

    print("HLT family:", args.hlt)
    print("special:", args.special)
    print("Eras:", eras_info)
    print("Input files:")
    for f in effList:
        print("  ", f)
    print("What to plot:", ", ".join(hlt_list))

    # 3) Loop su tutti i trigger fisici
    for trig in hlt_list:
        print(f"\n>>> Plot HLT = {trig}")
        effVsEras(
            inputList=effList,
            HLT=trig,
            legendList=legendList,
            isHadronic=isHadronic,
            version=args.version
        )


if __name__ == "__main__":
    main()
