import numpy as np
import os
import argparse
import ROOT

import skimNano as sn
import usefulFunc as uf

def parse_args():
    parser = argparse.ArgumentParser(description="HLT efficiency histogram builder")
    parser.add_argument("--inputDir", required=True, help="Directory with NanoAOD input ROOT files (trailing slash required)")
    parser.add_argument("--era", required=True, help="Run era (e.g. 2025C, 2024I)")
    parser.add_argument("--outVersion", required=True, help="Output subfolder name")
    parser.add_argument("--isHadronic", action="store_true", help="Use hadronic triggers (default: leptonic triggers)")
    parser.add_argument("--offline", default="ttH", help='Offline selection: "ttH", "ttbar", or a custom selection string')
    parser.add_argument("--isTest", action="store_true", help="Run in test mode (process only 10k events)")
    parser.add_argument("--ifMuonHLT", action="store_true", help="Use muon HLT (for lepton mode)")
    parser.add_argument("--otherCuts", action="store", default="", help="to select on the run")
    return parser.parse_args()

def main():
    args = parse_args()

    offline_map = {
        "ttH": "HT>500. && nj>=5 && nb>=1 && HLT_IsoMu24==1 && jet_4pt>40.", #tmp removal of jet_6pt>40 because I am not sure about this selection
        "ttbar_ele": "ne==1 && ele_1pt>16. && nj>=2 && nb>=1 && HLT_IsoMu24==1 && HT>200.",
        "ttbar_mu": "nm==1 && muon_1pt>14. && nj>=2 && nb>=1 && HLT_Ele30_WPTight_Gsf==1 && HT>200."
    }
    offline = offline_map.get(args.offline, args.offline)
    
    if args.otherCuts:
        offline = f"({offline}) && ({args.otherCuts})"

    print(f"Offline cut: {offline}")

    outFile = create_output_file(args.inputDir, args.outVersion, args.isTest)

    if args.isHadronic:
        run_hadronic_analysis(args.inputDir, outFile, args.era, offline)
        print("Running hadronic analysis")
    else:
        run_leptonic_analysis(args.inputDir, outFile, offline, args.era, args.ifMuonHLT)
        print("Running leptonic analysis")

def run_hadronic_analysis(inputDir, outFile, era, offline):
    df = ROOT.RDataFrame('Events', inputDir + '*.root')
    print('Initial entries:', df.Count().GetValue())

    hlt = {
        '1b': "HLT_PFHT450_SixPFJet36_PNetBTag0p35",
        '2b': "HLT_PFHT400_SixPFJet32_PNet2BTagMean0p50",
        '3b': sn.triggerSwitchedMap[era],
        'HH': "HLT_PFHT250_QuadPFJet25_PNet2BTagMean0p55"
    }

    bins = {
        'HT': np.array((500., 550, 600., 700., 800, 900., 2000)),
        'jet_6pt': np.array((0., 25, 50, 75, 100., 300.)),
        'nb': np.array((0.5, 1.5, 2.5, 3.5, 4.5, 8.5))
    }

    variables = [
        ('HT', bins['HT'], 'H_{T}(GeV)'),
        ('jet_6pt', bins['jet_6pt'], 'p_{T}^{6th jet}(GeV)'),
        ('nb', bins['nb'], 'n_{b-jet}')
    ]

    histList = []

    for var, binning, title in variables:
        histList += make_hist_pair(df, offline, f"{hlt['1b']}||{hlt['2b']}||{hlt['3b']}", var, title, binning, 'HLTAll')
        for nbcat, tag in zip(['==1', '==2', '==3', '>3'], ['1b', '2b', '3b', '4b']):
            trigger = hlt['1b'] if tag == '1b' else hlt['2b'] if tag == '2b' else hlt['3b']
            histList += make_hist_pair(df, f"{offline} && nb{nbcat}", trigger, var, title, binning, f"HLTAll_{tag}")
        histList += make_hist_pair(df, offline, hlt['HH'], var, title, binning, 'HH')

    write_histograms(histList, outFile)

def run_leptonic_analysis(inputDir, outFile, offline, era, ifMuonHLT):
    df = ROOT.RDataFrame('Events', inputDir + '*.root')
    print('Initial entries:', df.Count().GetValue())

    if ifMuonHLT:
        single, cross, lep, label = 'HLT_IsoMu24', 'HLT_Mu12_IsoVVL_PFHT150_PNetBTag0p53', 'muon', 'Mu'
        print("Lepton is muon")
    else:
        single, cross, lep, label = 'HLT_Ele30_WPTight_Gsf', 'HLT_Ele14_eta2p5_IsoVVVL_Gsf_PFHT200_PNetBTag0p53', 'ele', 'Ele'
        print("Lepton is electron")

    bins = {
        # Old Binning ##################
        # 'pt': np.array((0., 16, 20, 25, 30, 35, 45, 300)),
        # 'eta': np.array((-2.5, -2.2, -1.8, -1.4, -1.0, -0.6, 0.6, 1.0, 1.4, 1.8, 2.2, 2.5)),
        # 'HT': np.array((0., 100, 125, 150, 175, 200, 225, 250, 300, 350, 400, 500, 1000))
        ################################
        'pt': np.array((0., 16, 20, 25, 30, 35, 45, 65, 100, 200, 300)),
        'eta': np.array((-2.5, -2.2, -1.8, -1.4, -1.0, -0.6, 0.6, 1.0, 1.4, 1.8, 2.2, 2.5)),
        'HT': np.array((0., 100, 125, 150, 175, 200, 225, 250, 300, 350, 400, 500, 750, 1000))

    }

    variables = [
        (f"{lep}_1pt", bins['pt'], f"p_{{T}}^{{1st lep}}(GeV)"),
        (f"{lep}_1eta", bins['eta'], f"#eta^{{1st lep}}"),
        ('HT', bins['HT'], f"H_{{T}}")
    ]

    histList = []
    for var, binning, title in variables:
        histList += make_hist_pair(df, offline, single, var, title, binning, f"HLTsingle{label}")
        histList += make_hist_pair(df, offline, cross, var, title, binning, f"HLTcross{label}")
        histList += make_hist_pair(df, offline, f"{single}||{cross}", var, title, binning, f"HLTboth{label}")

    write_histograms(histList, outFile)

def make_hist_pair(df, offline, HLT, variable, title, bins, tag):
    # print("Creating histogram pairs")
    df_sel = df.Filter(offline)
    bins = np.array(bins, dtype='float64')
    de = df_sel.Histo1D((f"de_{variable}_{tag}", title, len(bins) - 1, bins), variable)
    nu = df_sel.Filter(HLT).Histo1D((f"nu_{variable}_{tag}", title, len(bins) - 1, bins), variable)
    return [de, nu]

def create_output_file(inputDir, version, isTest):
    outDir = os.path.join(inputDir if not isTest else 'output/', 'result', version)
    os.makedirs(outDir, exist_ok=True)
    print(f"Results will be written in {outDir}")
    return ROOT.TFile(os.path.join(outDir, 'eff.root'), 'RECREATE')

def write_histograms(histList, outFile):
    for h in histList:
        h.Print()
        h.SetDirectory(outFile)
    outFile.Write()
    print('Written:', outFile.GetName())
    outFile.Close()

if __name__ == '__main__':
    timer = ROOT.TStopwatch()
    timer.Start()
    main()
    timer.Stop()
    timer.Print()
