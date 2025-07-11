import numpy as np
import os
import ROOT

import skimNano as sn
import usefulFunc as uf

def main():
    # isTest = True
    isTest =False
    # inputDir = '/eos/home-h/hhua/forTopHLT/2024D/v1ForHadronic/'
    # inputDir = '/eos/home-h/hhua/forTopHLT/2024D/v2HadronicWithRdataframe/'
    # inputDir = '/eos/home-h/hhua/forTopHLT/2024E/v2HadronicWithRdataframe/'
    # inputDir = '/eos/home-h/hhua/forTopHLT/2024C/v2HadronicWithRdataframe/'
    # inputDir = '/eos/home-h/hhua/forTopHLT/2024F/v1ForHadronic/'
    # inputDir = '/eos/user/h/hhua/forTopHLT/2024F/v1ForHadronic/'
    # inputDir = '/eos/user/h/hhua/forTopHLT/2024G/v1ForHadronic_partial/'
    # inputDir = '/eos/user/h/hhua/forTopHLT/2024G/v1ForHadronic/'
    # inputDir = '/eos/user/h/hhua/forTopHLT/2024H/v1ForHadronic/'
    # inputDir = '/eos/user/h/hhua/forTopHLT/2024I/v1ForHadronic/'
    # inputDir = '/eos/user/h/hhua/forTopHLT/2024C/v1ForHadronicV2/'
    # inputDir = '/eos/user/h/hhua/forTopHLT/2024D/v1ForHadronicV2/'
    # inputDir = '/eos/user/h/hhua/forTopHLT/2024E/v1ForHadronicV2/'
    # inputDir = '/eos/user/h/hhua/forTopHLT/2024F/v1ForHadronicV2/'
    # #!what's the difference between /home-h and /user/h/hhua?
    # isHadronic = True
    # outVersion = 'v0ttHPhasephase'
    # offline = "HT>500. && nj>5 && nb>1 && HLT_IsoMu24==1 && jet_6pt>40." #ttH phase space
    # outVersion = 'v0ttHPhasephase'
    # outVersion = 'v0ttHPhasephase_preMD3'
    # outVersion = 'v0ttHPhasephase_postMD3'
   
    #for electron HLT efficiency measurement
    # inputDir = '/eos/home-h/hhua/forTopHLT/2024D/v1EleTTPhase/'
    # inputDir = '/eos/home-h/hhua/forTopHLT/2024E/v1EleTTPhase/'
    # inputDir = '/eos/user/h/hhua/forTopHLT/2024F/v1EleTTPhase/'
    # inputDir = '/eos/user/h/hhua/forTopHLT/2024G/v1EleTTPhase/'
    # inputDir = '/eos/user/h/hhua/forTopHLT/2024H/v1EleTTPhase/'
    # inputDir = '/eos/user/h/hhua/forTopHLT/2024I/v1EleTTPhase/'
    # outVersion = 'v0tt'
    # isHadronic = False
    # ifMuonHLT = False
    # offline = 'ne==1 && ele_1pt>16. && nj>2 && nb>1 && HLT_IsoMu24==1'#ttbar phase space 
    # offline = f"{offline} && HT>200."
    # offline = f'{offline} && run>384918 '#!MD3 in 2024G
    # outVersion = 'v1ttAndHT200'
    # outVersion = 'v1ttAndHT200_postMD3'
    # offline = f'{offline} && run<=384918 '#!MD3 in 2024G
    # offline = f'{offline} && run>384918 '#!MD3 in 2024G
    # outVersion = 'v1ttAndHT200_preMD3'
  
    #for muon HLT efficiency measurement
    # inputDir = '/eos/user/h/hhua/forTopHLT/2024F/v1MuonTTPhase/'
    # inputDir = '/eos/user/h/hhua/forTopHLT/2024G/v1MuonTTPhase/'
    # inputDir = '/eos/user/h/hhua/forTopHLT/2024H/v1MuonTTPhase/'
    inputDir = '/eos/user/h/hhua/forTopHLT/2024E/v1MuonTTPhase/'
    # inputDir = '/eos/user/h/hhua/forTopHLT/2024D/v1MuonTTPhase/'
    # inputDir = '/eos/user/h/hhua/forTopHLT/2024I/v1MuonTTPhase/'
    offline = 'nm==1 && muon_1pt>14. && nj>2 && nb>1 && HLT_Ele30_WPTight_Gsf==1'#ttbar phase space
    offline = f"{offline} && HT>200."
    outVersion = 'v1ttAndHT200'
    isHadronic = False
    ifMuonHLT = True
  
  
  
   
    era = uf.extract_era_from_path(inputDir)
    print('era: ', era)
    outFile = makeOutFile(inputDir, isTest, outVersion) 
    if isHadronic:
        HLTHistFill(inputDir, outFile, isHadronic, isTest, era,  offline)#!using rDataframe for fasting processing
    else:
        HLTHistFill_ele(inputDir, outFile, isTest, era, offline, ifMuonHLT)
   
    # oldEventLoopSel(inputDir, outFile) # put old event loop here

def HLTHistFill_ele(inputDir, outFile, isTest, era, offline, ifMuonHLT=False):
    df = ROOT.RDataFrame('Events', inputDir+'*.root')
    print('inputDir: ', inputDir)
    print('initial entries: ', df.Count().GetValue())
    
    singleEle = 'HLT_Ele30_WPTight_Gsf'
    eleCross = 'HLT_Ele14_eta2p5_IsoVVVL_Gsf_PFHT200_PNetBTag0p53'
    offlineLep = 'ele'
    lepName = 'e'
    HLTName = 'Ele'
    if ifMuonHLT:
        singleEle = 'HLT_IsoMu24'
        eleCross = 'HLT_Mu12_IsoVVL_PFHT150_PNetBTag0p53' 
        offlineLep = 'muon' 
        lepName = '#mu'
        HLTName = 'Mu'
    
    ptBin = np.array((0., 16, 20, 25, 30, 35, 45, 300))
    de_ele1pt, nu_ele1pt = getDeAndNuHist(df, offline, singleEle, f"{offlineLep}_1pt", 'p_{T}^{1st lep}(GeV)', ptBin, f'HLTsingle{HLTName}')
    de_ele1ptCross, nu_ele1ptCross = getDeAndNuHist(df, offline, eleCross, f"{offlineLep}_1pt", 'p_{T}^{1st lep}(GeV)', ptBin, f'HLTcross{HLTName}')
    # de_ele1pt_both, nu_ele1pt_both = getDeAndNuHist(df, offline, f"{singleEle}||{eleCross}", f"{offlineLep}_1pt", 'p_{T}^{1st lep}(GeV)', ptBin, 'HLTbothEle')
    de_ele1pt_both, nu_ele1pt_both = getDeAndNuHist(df, offline, f"{singleEle}||{eleCross}", f"{offlineLep}_1pt", 'p_{T}^{1st lep}(GeV)', ptBin, f'HLTboth{HLTName}')
    
    etaBin = np.array((-2.5, -2.2, -1.8, -1.4, -1.0, -0.6, 0.6, 1.0, 1.4, 1.8, 2.2, 2.5)) 
    de_ele1etaCross, nu_ele1etaCross = getDeAndNuHist(df, offline, eleCross, f"{offlineLep}_1eta", '#eta^{1st lep}', etaBin, f'HLTcross{HLTName}')
    de_ele1eta_single, nu_ele1eta_single = getDeAndNuHist(df, offline, singleEle, f"{offlineLep}_1eta", '#eta^{1st lep}', etaBin, f'HLTsingle{HLTName}')
    de_ele1eta_both, nu_ele1eta_both = getDeAndNuHist(df, offline, f"{singleEle}||{eleCross}", f"{offlineLep}_1eta", '#eta^{1st lep}', etaBin, f'HLTboth{HLTName}')
    
    # HTBin = np.array((0., 50, 100, 150, 200, 250, 350, 1000))
    HTBin = np.array((0., 100, 125, 150, 175, 200, 225, 250, 300, 350, 400, 500, 1000))
    de_HT, nu_HT = getDeAndNuHist(df, offline, singleEle, "HT", 'HT(GeV)', HTBin, f'HLTsingle{HLTName}')
    de_HTCross, nu_HTCross = getDeAndNuHist(df, offline, eleCross, "HT", 'HT(GeV)', HTBin, f'HLTcross{HLTName}')
    de_HT_both, nu_HT_both = getDeAndNuHist(df, offline, f"{singleEle}||{eleCross}", "HT", 'HT(GeV)', HTBin, f'HLTboth{HLTName}')
    
    histList = [de_ele1pt, nu_ele1pt, de_ele1ptCross, nu_ele1ptCross, de_ele1pt_both, nu_ele1pt_both, de_ele1etaCross, nu_ele1etaCross, de_HT, nu_HT, de_HTCross, nu_HTCross, de_HT_both, nu_HT_both, de_ele1eta_single, nu_ele1eta_single, de_ele1eta_both, nu_ele1eta_both]
    writeToFile(histList ,outFile)
    
    
def HLTHistFill(inputDir, outFile, isHadronic, isTest, era, offline='HT>500. && nj>5 && nb>1 && HLT_IsoMu24==1'):
    df = ROOT.RDataFrame('Events', inputDir+'*.root')
    print('inputDir: ', inputDir)
    print('initial entries: ', df.Count().GetValue())
    
    
    HLT_1btag = "HLT_PFHT450_SixPFJet36_PNetBTag0p35"
    HLT_2btag = "HLT_PFHT400_SixPFJet32_PNet2BTagMean0p50"
    # HLT_3btag = "HLT_PFHT330PT30_QuadPFJet_75_60_45_40_PNet3BTag_4p3"
    HLT_3btag = sn.triggerSwitchedMap[era]
    HLT_all = f"{HLT_1btag}||{HLT_2btag}||{HLT_3btag}"
    # HLT_HH = 'HLT_PFHT280_QuadPFJet30_PNet2BTagMean0p55'
    HLT_HH = 'HLT_PFHT250_QuadPFJet25_PNet2BTagMean0p55'
    
    binning = np.array((500., 550, 600.,  700., 800, 900. , 2000)) 
    jet6ptBin = np.array((0., 25, 50, 75, 100.,  300., ))
    nbBin = np.array((0.5, 1.5, 2.5, 3.5, 4.5, 8.5))
    de_HT, nu_HT = getDeAndNuHist(df, offline, HLT_all, "HT", 'HT(GeV)', binning, 'HLTAll')
    # de_jet6pt, nu_jet6pt = getDeAndNuHist(df, offline, HLT_all, "jet_6pt", jet6ptBin, 'HLTAll')
    # de_nb, nu_nb = getDeAndNuHist(df, offline, HLT_all, "nb", nbBin, 'HLTAll')
    de_jet6pt, nu_jet6pt = getDeAndNuHist(df, offline, HLT_all, "jet_6pt", 'p_{T}^{6th jet}(GeV)', jet6ptBin, 'HLTAll')
    de_nb, nu_nb = getDeAndNuHist(df, offline, HLT_all, "nb", 'n_{b-jet}', nbBin, 'HLTAll')
    
    #For efficincy in different b multiplicity regions 
    # de_HT_2b, nu_HT_2b = getDeAndNuHist(df, f"{offline} && nb==2", HLT_2btag, "HT", binning, 'HLTAll_2b')
    # de_HT_3b, nu_HT_3b = getDeAndNuHist(df, f"{offline} && nb==3", HLT_3btag, "HT", binning, 'HLTAll_3b')
    # de_HT_4b, nu_HT_4b = getDeAndNuHist(df, f"{offline} && nb>3", HLT_3btag, "HT", binning, 'HLTAll_4b')
    # de_jet6pt_2b, nu_jet6pt_2b = getDeAndNuHist(df, f"{offline} && nb==2", HLT_2btag, "jet_6pt", jet6ptBin, 'HLTAll_2b')
    # de_jet6pt_3b, nu_jet6pt_3b = getDeAndNuHist(df, f"{offline} && nb==3", HLT_3btag, "jet_6pt", jet6ptBin, 'HLTAll_3b')
    # de_jet6pt_4b, nu_jet6pt_4b = getDeAndNuHist(df, f"{offline} && nb>3", HLT_3btag, "jet_6pt", jet6ptBin, 'HLTAll_4b')
    
    de_HT_HH, nu_HT_HH = getDeAndNuHist(df, offline, HLT_HH, "HT", 'HT(GeV)', binning, 'HH')
    de_jet6pt_HH, nu_jet6pt_HH = getDeAndNuHist(df, offline, HLT_HH, "jet_6pt", 'p_{T}^{6th jet}(GeV)',jet6ptBin, 'HH')
    de_nb_HH, nu_nb_HH = getDeAndNuHist(df, offline, HLT_HH, "nb", 'n_{b-jet}', nbBin, 'HH')
    
    
    histList = [de_HT, nu_HT, de_jet6pt, nu_jet6pt, de_nb, nu_nb,  de_HT_HH, nu_HT_HH, de_jet6pt_HH, nu_jet6pt_HH, de_nb_HH, nu_nb_HH]
    writeToFile(histList ,outFile)                                                               
    
# def getDeAndNuHist(df, offline, HLT, variable, binning, namePost=''):
def getDeAndNuHist(df, offline, HLT, variable, variableTitle, binning, namePost=''):
    df = df.Filter(offline)
    # de = df.Histo1D((f"de_{variable}_{namePost}", variable, len(binning)-1, binning), variable)
    # nu = df.Filter(HLT).Histo1D((f"nu_{variable}_{namePost}", variable, len(binning)-1, binning), variable)
    de = df.Histo1D((f"de_{variable}_{namePost}", variableTitle, len(binning)-1, binning), variable)
    nu = df.Filter(HLT).Histo1D((f"nu_{variable}_{namePost}", variableTitle, len(binning)-1, binning), variable)
    return de, nu
                                                                       
def writeToFile(histList, outFile):
    for ih in histList:
        ih.Print()
        ih.SetDirectory(outFile)
    outFile.Write()
    print('outFile here: ', outFile.GetName())
    outFile.Close()                                                               
    
    
    
    
def oldEventLoopSel():
    print('inputDir: ', inputDir)
    chain = ROOT.TChain('Events')
    chain.Add(inputDir+'*.root')
    entries = chain.GetEntries()
    print('entries: ', entries)
  
    if isHadronic:
        histList = makeHist_hard(chain, isTest, era) 
    else:
        histList = makeHist_ele(chain, isTest)
  
   
    for ih in histList:
        ih.Print()
        ih.SetDirectory(outFile)
    
    print('outFile here: ', outFile.GetName())
    outFile.Write()
    outFile.Close()

def makeHist_ele(chain, isTest):
    binning_e = np.array((0.,25., 30., 35.,40.,45.,50.,60.,80.,120.,200.,400.))
    de_eleJet = ROOT.TH1D('de_ele1pt_eleJet', 'p_{T}^{1st e}(GeV)', len(binning_e)-1,binning_e)
    nu_eleJet = ROOT.TH1D('nu_ele1pt_eleJet', 'p_{T}^{1st e}(GeV)', len(binning_e)-1,binning_e)
    de_eleHT = ROOT.TH1D('de_ele1pt_eleHT', 'p_{T}^{1st e}(GeV)', len(binning_e)-1,binning_e)
    nu_eleHT = ROOT.TH1D('nu_ele1pt_eleHT', 'p_{T}^{1st e}(GeV)', len(binning_e)-1,binning_e)

    # de_singleEleJet = ROOT.TH1D('de_ele1pt_eleJet', 'p_{T}^{1st e}(GeV)', len(binning_e)-1,binning_e)
    # nu_singleEleJet = ROOT.TH1D('nu_ele1pt_eleJet', 'p_{T}^{1st e}(GeV)', len(binning_e)-1,binning_e)
    # de_singleEleHT = ROOT.TH1D('de_ele1pt_eleHT', 'p_{T}^{1st e}(GeV)', len(binning_e)-1,binning_e)
    # nu_singleEleHT = ROOT.TH1D('nu_ele1pt_eleHT', 'p_{T}^{1st e}(GeV)', len(binning_e)-1,binning_e)
    
    
    entries = chain.GetEntries()
    if isTest:
        entries = 10000
    for entry in range(entries):
        chain.GetEntry(entry)
        nj_ele, HT = sn.jetSel(chain) 
        ne = sn.getEleNum(chain)
        if((nj_ele > 0) & (ne>0)):
            de_eleJet.Fill(chain.Electron_pt[0])
            # de_singleEleJet.Fill(chain.Electron_pt[0])
            if(chain.HLT_Ele30_eta2p1_WPTight_Gsf_CentralPFJet35_EleCleaned==1):
                nu_eleJet.Fill(chain.Electron_pt[0])
            # if(chain.HLT_Ele30_WPTight_Gsf==1):
            #     nu_singleEleJet.Fill(chain.Electron_pt[0])
        
        if((nj_ele > 1) & (ne>0) & (HT>200.) ):
            de_eleHT.Fill(chain.Electron_pt[0])
            # de_singleEleHT.Fill(chain.Electron_pt[0])
            if(chain.HLT_Ele28_eta2p1_WPTight_Gsf_HT150==1):
                nu_eleHT.Fill(chain.Electron_pt[0])
            # if(chain.HLT_Ele30_WPTight_Gsf==1):
            #     nu_singleEleHT.Fill(chain.Electron_pt[0])
    histList = [de_eleHT, nu_eleHT, de_eleJet, nu_eleJet]#, de_singleEleHT, nu_singleEleHT, de_singleEleJet, nu_singleEleJet,]
    return histList    
    

def makeHist_hard(chain, isTest, era):
    #!!!should switch to TEfficiency for efficiency calculation
    de_jetNum = ROOT.TH1D('de_jetNum', 'n^{jet}', 6, 6, 12)
    nu_jetNum_1btag =  ROOT.TH1D('nu_jetNum_1btag', 'n^{jet}', 6, 6, 12)
    nu_jetNum_2btag = ROOT.TH1D('nu_jetNum_2btag', 'n^{jet}', 6, 6, 12)
    nu_jetNum_both = ROOT.TH1D('nu_jetNum_both', 'n^{jet}', 6, 6, 12)

    binning = np.array((2., 3., 4., 5., 7.))
    de_bjetNum = ROOT.TH1D('de_bjetNum', 'n^{b-jet}', len(binning)-1, binning)
    nu_bjetNum_1btag =  ROOT.TH1D('nu_bjetNum_1btag', 'n^{b-jet}', len(binning)-1, binning)
    nu_bjetNum_2btag = ROOT.TH1D('nu_bjetNum_2btag', 'n^{b-jet}', len(binning)-1, binning)
    nu_bjetNum_both = ROOT.TH1D('nu_bjetNum_both', 'n^{b-jet}', len(binning)-1, binning)
    
    #binning = np.array((500., 550., 600., 650., 700., 800., 900., 1000., 1300., 2000)) 
    binning = np.array((550., 600., 650., 700., 800., 900., 1000., 1300., 2000)) 
    de_HT = ROOT.TH1D('de_HT', 'HT(GeV)', len(binning)-1, binning)
    nu_HT_1btag =  ROOT.TH1D('nu_HT_1btag', 'HT(GeV)', len(binning)-1, binning)
    nu_HT_2btag = ROOT.TH1D('nu_HT_2btag', 'HT(GeV)', len(binning)-1, binning)
    nu_HT_both = ROOT.TH1D('nu_HT_both', 'HT(GeV)', len(binning)-1, binning)
    
    entries = chain.GetEntries()
    if isTest:
        entries = 10000
    for entry in range(entries):
        chain.GetEntry(entry)
        
        #!!!change to era dependant
        if era =='2023C' or era =='2023B' or era=='2022':
            HLT_1btag = chain.HLT_PFHT450_SixPFJet36_PFBTagDeepJet_1p59
            HLT_2btag = chain.HLT_PFHT400_SixPFJet32_DoublePFBTagDeepJet_2p94
            btag = 0
        else: 
            HLT_1btag = chain.HLT_PFHT450_SixPFJet36_PNetBTag0p35
            HLT_2btag = chain.HLT_PFHT400_SixPFJet32_PNet2BTagMean0p50
            btag = 1

        #QuadPFJet triggers for checking combined 1btag OR 2btag efficiency
        HLT_4jet = False
        HLT_4jet1 = False
        HLT_4jet2 = False
        if chain.GetBranch("HLT_QuadPFJet70_50_40_35_PFBTagParticleNet_2BTagSum0p65"):
            HLT_4jet = chain.HLT_QuadPFJet70_50_40_35_PFBTagParticleNet_2BTagSum0p65
        if chain.GetBranch("HLT_QuadPFJet70_50_40_35_PNet2BTagMean0p65"):
            HLT_4jet1 = chain.HLT_QuadPFJet70_50_40_35_PNet2BTagMean0p65
        if chain.GetBranch("HLT_PFHT280_QuadPFJet30_PNet2BTagMean0p55"):
            HLT_4jet2 = chain.HLT_PFHT280_QuadPFJet30_PNet2BTagMean0p55
        
    #preslection
        jetNum, HT = jetSel(chain)
        bjetNum, bHT = jetSel(chain, True, btag)
        if ( not (jetNum>5 and HT>550 and bjetNum>1)):
            continue
        
        de_jetNum.Fill(jetNum)
        de_HT.Fill(HT)
        de_bjetNum.Fill(bjetNum)
      
            
            
            
        if HLT_1btag:# and not HLT_2btag:
            nu_jetNum_1btag.Fill(jetNum)
            nu_bjetNum_1btag.Fill(bjetNum)
            nu_HT_1btag.Fill(HT)
        if HLT_2btag:# and not HLT_1btag:
            nu_jetNum_2btag.Fill(jetNum)
            nu_bjetNum_2btag.Fill(bjetNum)
            nu_HT_2btag.Fill(HT)
        if era=='2022':
            if HLT_2btag or HLT_1btag or HLT_4jet:
                nu_jetNum_both.Fill(jetNum)
                nu_bjetNum_both.Fill(bjetNum)
                nu_HT_both.Fill(HT)
        else:
            if HLT_2btag or HLT_1btag or HLT_4jet1 or HLT_4jet2:
                nu_jetNum_both.Fill(jetNum)
                nu_bjetNum_both.Fill(bjetNum)
                nu_HT_both.Fill(HT)
            
            
    histList = [de_jetNum, nu_jetNum_1btag, nu_jetNum_2btag, nu_jetNum_both, de_bjetNum, nu_bjetNum_1btag, nu_bjetNum_2btag, nu_bjetNum_both, de_HT, nu_HT_1btag, nu_HT_2btag, nu_HT_both]
    return histList
        
    
    
def makeOutFile(inputDir, isTest, outVersion='v0'):
    outDir = inputDir+ 'result/'
    #outDir = inputDir+ 'resultBPix/'
    if isTest:
        outDir = 'output/'
    if not os.path.exists(outDir):
        os.makedirs(outDir)
    outDir = outDir + outVersion + '/'
    os.makedirs(outDir) if not os.path.exists(outDir) else None
    outFile = ROOT.TFile(outDir+'eff.root', 'RECREATE')
    return outFile
    
      
def preSel( chain) :
    # for Jet in range(0,chain.nJet):
    #     if abs(chain.Jet_eta[Jet])>2.4: 
    #         continue
    #     if chain.Jet_pt[Jet]<30: 
    #         continue
    #     # chain ht
    #     if((chain.Jet_pt[Jet] > 30.) & (abs(chain.Jet_eta[Jet])<2.4)): 
    #         ht = ht + chain.Jet_pt[Jet]
    #     # nJets
    #     if((chain.Jet_pt[Jet] > 40.) & (abs(chain.Jet_eta[Jet])<2.4) ):
    #         nj = nj+1
    #     # nbJets
    #     if((chain.Jet_pt[Jet] > 40.) & (abs(chain.Jet_eta[Jet])<2.4) & (chain.Jet_btagDeepFlavB[Jet]>0.2770)):
    #         nb = nb+1
        # if((chain.Jet_pt[Jet] > 40.) & (abs(chain.Jet_eta[Jet])<2.4) & (chain.Jet_btagdeepb[Jet]>0.4941)):##!!!
        # if((chain.Jet_pt[Jet] > 40.) & (abs(chain.Jet_eta[Jet])<2.4) & (chain.Jet_btagPNetB[Jet]>0.4941)):##!!!
        
    jetNum, HT = jetSel(chain)
    bjetNum, bHT = jetSel(chain, True)
        
    # ifPass = (nj > 5)  & (nb>1) & (ht>500) & (chain.HLT_IsoMu24==1)
    # ifPass = jetNum>5 and HT>500 and bjetNum>1 and chain.HLT_IsoMu24==1
    ifPass = jetNum>5 and HT>500 and bjetNum>0 and chain.HLT_IsoMu24==1
    return ifPass

def jetSel(chain, isB=False, btag=0):
    jetNum = 0
    HT = 0
    for i in range(0, chain.nJet):
        if( not ((chain.Jet_pt[i] > 40.) and (abs(chain.Jet_eta[i])<2.4))) :
        #if( not ((chain.Jet_pt[i] > 40.) and (abs(chain.Jet_eta[i])<2.4) and (chain.Jet_eta[i]<-1.8 or chain.Jet_eta[i]>0.6))) :
            continue
        if isB:
            # DeepJet 0.355; PNet: 0.387
        #!!!change to era dependant
            if btag == 0:
                if( not (chain.Jet_btagDeepFlavB[i]>0.355)):
                    continue
            if btag==1:
                if( not (chain.Jet_btagPNetB[i]>0.387)):
                    continue
                
        jetNum+=1
        HT = HT+ chain.Jet_pt[i] 
        # print(HT, chain.Jet_pt[i])
    return jetNum, HT 
    
           
    

if __name__=='__main__':
    t = ROOT.TStopwatch()
    t.Start()
    main()
    t.Stop()
    t.Print()
