import ROOT
import os
import argparse

import usefulFunc as uf

triggerSwitchedMap = {
    '2024C': 'HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepJet_4p5',
    '2024D': 'HLT_PFHT330PT30_QuadPFJet_75_60_45_40_PNet3BTag_4p3',
    '2024E': 'HLT_PFHT330PT30_QuadPFJet_75_60_45_40_PNet3BTag_4p3',
    '2024F': 'HLT_PFHT330PT30_QuadPFJet_75_60_45_40_PNet3BTag_4p3',
    '2024G': 'HLT_PFHT330PT30_QuadPFJet_75_60_45_40_PNet3BTag_4p3',
    '2024I': 'HLT_PFHT330PT30_QuadPFJet_75_60_45_40_PNet3BTag_4p3',
    '2024H': 'HLT_PFHT330PT30_QuadPFJet_75_60_45_40_PNet3BTag_4p3',
} 

def main(inputNano = '/store/data/Run2023B/Muon0/NANOAOD/PromptNanoAODv11p9_v1-v2/60000/06d25571-df3e-4ceb-9e44-7452add3e004.root', outDir = './output/', ifForHadronic = True,   ifTest = True):
    #!test default input files in parse_arguments()
    print('inputNano: ', inputNano)
    print('outDir: ', outDir, 'ifForHadronic: ', ifForHadronic, 'ifTest: ', ifTest)
    inputNano = 'root://cmsxrootd.fnal.gov/'+ inputNano
    preSel(inputNano,  outDir, ifForHadronic, ifTest)#faster run time with rDataFrame
    
    # selLoop(chain, branches_to_keep, outDir, ifForHadronic, ifTest)#!obsolete, keep it for now
    
def preSel(inputNano,  outDir, ifForHadronic, ifTest):
    #faster and better with rDataFrame:)
    ROOT.gInterpreter.Declare("""
    #include <vector>
    #include "Math/Vector4D.h"
        auto jetSelNew = [](const ROOT::VecOps::RVec<float>& Jet_pt, const ROOT::VecOps::RVec<float>& Jet_eta, 
                    const ROOT::VecOps::RVec<float>& Jet_phi, const ROOT::VecOps::RVec<float>& Jet_mass, const ROOT::VecOps::RVec<float>& Jet_btagPNetB, Bool_t isB=kFALSE) { 
            std::vector<ROOT::Math::PtEtaPhiMVector> selectedJets;
            for (int i = 0; i < Jet_pt.size(); i++) {
                if (!(Jet_pt[i] > 25. && abs(Jet_eta[i]) < 2.4)) continue;
                if (isB) {
                    if (!(Jet_btagPNetB[i] > 0.387)) continue;
                } 
                selectedJets.emplace_back(Jet_pt[i], Jet_eta[i], Jet_phi[i], Jet_mass[i]);
            }
            return selectedJets;
        };
    """) 
    
    ROOT.gInterpreter.Declare("""
    auto HTCal = [](const std::vector<ROOT::Math::PtEtaPhiMVector>& jets) {
        double ht = 0.0;
        for (const auto& jet : jets) {
            ht += jet.Pt();
        }
        return ht;
    };
    """)
    
    ROOT.gInterpreter.Declare("""
                              auto eleSel = [](const ROOT::VecOps::RVec<float>& Electron_pt, const ROOT::VecOps::RVec<float>& Electron_eta, const ROOT::VecOps::RVec<float>& Electron_phi, const ROOT::VecOps::RVec<float>& Electron_mass,  const ROOT::VecOps::RVec<int>& Electron_cutBased) {
        std::vector<ROOT::Math::PtEtaPhiMVector> selectedElectrons;
            for (int i = 0; i < Electron_pt.size(); i++) {
                if (!(Electron_pt[i] > 10. && abs(Electron_eta[i]) < 2.4 && Electron_cutBased[i] >= 4)) continue;
                selectedElectrons.emplace_back(Electron_pt[i], Electron_eta[i], Electron_phi[i], Electron_mass[i]);
            }
            return selectedElectrons;
        };
    """)
    
    ROOT.gInterpreter.Declare("""
                              auto muonSel = [](const ROOT::VecOps::RVec<float>& Muon_pt, const ROOT::VecOps::RVec<float>& Muon_eta, const ROOT::VecOps::RVec<float>& Muon_phi, const ROOT::VecOps::RVec<float>& Muon_mass,  const ROOT::VecOps::RVec<bool>& Muon_tightId, const ROOT::VecOps::RVec<float>& Muon_pfRelIso04_all) {
        std::vector<ROOT::Math::PtEtaPhiMVector> selectedMuons;
            for (int i = 0; i < Muon_pt.size(); i++) {
                if (!(Muon_pt[i] > 10. && abs(Muon_eta[i]) < 2.4 && Muon_tightId[i] && Muon_pfRelIso04_all[i] < 0.15)) continue;
                selectedMuons.emplace_back(Muon_pt[i], Muon_eta[i], Muon_phi[i], Muon_mass[i]);
            }
            return selectedMuons;
        };
    """)
   
    
    print('input: ', inputNano) 
    df = ROOT.RDataFrame("Events", inputNano)
    # print(df.GetColumnNames())  
    print('initial events: ', df.Count().GetValue())
    if ifTest:
        df = df.Range(10000)
   
    # df = df.Filter('HLT_IsoMu24==1')#!can not have this for muon trigger
    
    df = df.Define('selectedJets', 'jetSelNew(Jet_pt, Jet_eta, Jet_phi, Jet_mass,  Jet_btagPNetB, kFALSE )')
    df = df.Define('selectedBjets', 'jetSelNew(Jet_pt, Jet_eta, Jet_phi, Jet_mass, Jet_btagPNetB, kTRUE )')
    df = df.Define('nj', '(int)selectedJets.size()')
    df = df.Define('nb', '(int)selectedBjets.size()')
    df = df.Define('jet_6pt', 'nj>5 ? selectedJets[5].Pt() : -1')
    df = df.Define("HT", "HTCal(selectedJets)")
    
    df = df.Define('selectedElectrons', 'eleSel(Electron_pt, Electron_eta, Electron_phi, Electron_mass, Electron_cutBased)')
    df = df.Define('ne', '(int)selectedElectrons.size()')
    df = df.Define('ele_1pt', 'ne>0 ? selectedElectrons[0].Pt() : -1')
    df = df.Define('ele_1eta', 'ne>0 ? selectedElectrons[0].Eta() : -1')
    df = df.Define('ele_1phi', 'ne>0 ? selectedElectrons[0].Phi() : -1')
    
    df = df.Define('selectedMuons', 'muonSel(Muon_pt, Muon_eta, Muon_phi, Muon_mass, Muon_tightId, Muon_pfRelIso04_all)')
    df = df.Define('nm', '(int)selectedMuons.size()')
    df = df.Define('muon_1pt', 'nm>0 ? selectedMuons[0].Pt() : -1')
    df = df.Define('muon_1eta', 'nm>0 ? selectedMuons[0].Eta() : -1')
    df = df.Define('muon_1phi', 'nm>0 ? selectedMuons[0].Phi() : -1')

    
    preSelect = 'nj>5 && HT>500. && nb>1'
    if not ifForHadronic:
        ifEleDataset = inputNano.find('EGamma')!=-1
        print('ifEleDataset: ', ifEleDataset)
        if not ifEleDataset:#for ele trigger
            preSelect = 'ne==1 && ele_1pt>16. && nj>2 && nb>1' #typical tt phase space
        else: 
            preSelect = 'nm==1 && muon_1pt>14 && nj>2 && nb>1' #typical tt phase space
        preSelect 
    df = df.Filter(preSelect)
    print('preselection: ', preSelect)
    
    
    if ifTest:
        outDir = './output/'
    if not os.path.exists(outDir):
        os.makedirs(outDir)
    
    # era = uf.getEra(inputNano)
    era = uf.getEraNano(inputNano)
    print('era: ', era)
       
    # List of branch names to keep
    branches_to_keep = [
                        #2023D
                        'HLT_PFHT450_SixPFJet36_PNetBTag0p35',
                        'HLT_PFHT400_SixPFJet32_PNet2BTagMean0p50',
                        triggerSwitchedMap[era],
                        # 'HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepJet_4p5', # ![ 378981, 380933], from HLT INFO GUI
                        # 'HLT_PFHT340_QuadPFJet70_50_40_40_PNet2BTagMean0p70', #3.2	[378981,380933] ; 2024C[37941, 380252]
                        # 'HLT_PFHT330PT30_QuadPFJet_75_60_45_40_PNet3BTag_4p3', ##!seems not available in 2024C, starting 379613
                        # 'HLT_PFHT280_QuadPFJet30_PNet2BTagMean0p55',#!ParkingHH since 2023C run 367661
                        'HLT_PFHT250_QuadPFJet25_PNet2BTagMean0p55',#!HT280 is the backup
                        'HLT_IsoMu24',
                        # 'HLT_Ele30_eta2p1_WPTight_Gsf_CentralPFJet35_EleCleaned',# !disabled in 2024
                        # 'HLT_Ele28_eta2p1_WPTight_Gsf_HT150', #!disabled in 2024
                        'HLT_Ele30_WPTight_Gsf',
                        'HLT_Ele14_eta2p5_IsoVVVL_Gsf_PFHT200_PNetBTag0p53', #!added in 2024C after run 379613
                        'HLT_Mu12_IsoVVL_PFHT150_PNetBTag0p53',#!added in 2024C after run 379613
                        "run",
                        ]
   
    #check in run branch>379613 in df, then remove the ele and mu trigger in the branches_to_keep
    # afterRun = df.Filter('run>379613') #Some files including this run, still don't have the lepton cross triggers
    # if afterRun.Count().GetValue() == 0:
    if era == '2024C':
        branches_to_keep.remove('HLT_Ele14_eta2p5_IsoVVVL_Gsf_PFHT200_PNetBTag0p53')
        branches_to_keep.remove('HLT_Mu12_IsoVVL_PFHT150_PNetBTag0p53')
    # print('afterRun: ', afterRun.Count().GetValue())
     
        
    branches_to_keep.append('nj')
    branches_to_keep.append('nb')    
    branches_to_keep.append('HT')
    branches_to_keep.append('jet_6pt')
    branches_to_keep.append('ne')
    branches_to_keep.append('ele_1pt')
    branches_to_keep.append('ele_1eta')
    branches_to_keep.append('ele_1phi')
    branches_to_keep.append('nm')
    branches_to_keep.append('muon_1pt')
    branches_to_keep.append('muon_1eta')
    branches_to_keep.append('muon_1phi')
    
    postFix = inputNano.rsplit("/", 1)[-1]
    df.Snapshot("Events", outDir+postFix, branches_to_keep)
    print('after selection: ', df.Count().GetValue())
    print('file saved here: ', outDir+postFix)
   
   
   
   
    
    

def process_arguments():
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description='Description of your script.')
 
    # input = '/store/data/Run2023B/Muon0/NANOAOD/PromptNanoAODv11p9_v1-v2/60000/06d25571-df3e-4ceb-9e44-7452add3e004.root'
    # input = '/store/data/Run2022C/Muon/NANOAOD/PromptNanoAODv10-v1/40000/d4484006-7e4b-424e-86a4-346d17d862f8.root'
    # input = '/store/data/Run2024E/Muon0/NANOAOD/PromptReco-v1/000/380/956/00000/8413549d-588b-46ff-9c53-b98b34faa7e7.root'
    # input = '/store/data/Run2024D/Muon0/NANOAOD/PromptReco-v1/000/380/346/00000/3c839fb5-92c1-4140-a9ab-1efe2ad80a60.root'
    input = '/store/data/Run2024C/Muon1/NANOAOD/PromptReco-v1/000/380/195/00000/0567ac8a-b6c6-466e-b0da-0474f2bbeea6.root'
    # input = '/store/data/Run2024F/Muon0/NANOAOD/PromptReco-v1/000/383/367/00000/407206b5-4ab2-45e4-a40b-0d150ff3263a.root'
    # input = '/store/data/Run2024F/EGamma1/NANOAOD/PromptReco-v1/000/382/165/00000/f5235ff3-bb75-4c73-8c6a-d1b1b5fcdf39.root'
    # input = '/store/data/Run2024G/Muon0/NANOAOD/PromptReco-v1/000/383/814/00000/c96be705-bd3e-4cde-8967-ed77e70a6424.root'
    # input = '/store/data/Run2024G/EGamma1/NANOAOD/PromptReco-v1/000/384/610/00000/765b14d1-f959-4a2e-8c75-6a91c75ca85f.root'#!seems problem with reading this file from jobs
    # Add arguments
    parser.add_argument('--input', type=str, default=input)
    parser.add_argument('--outDir', type=str, default='./output/')
    # parser.add_argument('--ifHardronic', type=bool, default=True)
    # parser.add_argument('--ifTest', type=bool, default=True)
    parser.add_argument('--ifHardronic', type=str2bool, default=True, help='Boolean flag for hadronic')
    parser.add_argument('--ifTest', type=str2bool, default=True, help='Boolean flag for test mode')


      # Parse the command-line arguments
    args = parser.parse_args()

    # Access the parsed arguments
    arguments = {
        'input': args.input,
        'outDir': args.outDir,
        'ifHardronic': args.ifHardronic,
        'ifTest': args.ifTest
    }

    return arguments


def str2bool(value):
    """Convert a string representation of truth to true/false."""
    if isinstance(value, bool):
        return value
    if value.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif value.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


if __name__=='__main__':
    args = process_arguments()
    main(args['input'], args['outDir'], args['ifHardronic'], args['ifTest'])

