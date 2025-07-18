import os
import ROOT
import plotHelper as ph
import usefulFunc as uf


def main():
    # in2024D = '/eos/home-h/hhua/forTopHLT/2024D/v2HadronicWithRdataframe/result/eff.root'
    # in2024E = '/eos/home-h/hhua/forTopHLT/2024E/v2HadronicWithRdataframe/result/eff.root'
    # in2024C = '/eos/home-h/hhua/forTopHLT/2024C/v2HadronicWithRdataframe/result/eff.root'
    # ifHadronic =True
    # effList = [
    # #     '/eos/home-h/hhua/forTopHLT/2024C/v2HadronicWithRdataframe/result/v0ttHPhasephase/eff.root',
    # #     '/eos/home-h/hhua/forTopHLT/2024D/v2HadronicWithRdataframe/result/v0ttHPhasephase/eff.root',
    # #     '/eos/home-h/hhua/forTopHLT/2024E/v2HadronicWithRdataframe/result/v0ttHPhasephase/eff.root',
    #         '/eos/user/h/hhua/forTopHLT/2024F/v1ForHadronic/result/v0ttHPhasephase/eff.root',
        #    '/eos/user/h/hhua/forTopHLT/2024C/v1ForHadronicV2/result/v0ttHPhasephase/eff.root',
        #    '/eos/user/h/hhua/forTopHLT/2024D/v1ForHadronicV2/result/v0ttHPhasephase/eff.root',
        #    '/eos/user/h/hhua/forTopHLT/2024E/v1ForHadronicV2/result/v0ttHPhasephase/eff.root',
        #    '/eos/user/h/hhua/forTopHLT/2024F/v1ForHadronicV2/result/v0ttHPhasephase/eff.root',
        #    '/eos/user/h/hhua/forTopHLT/2024G/v1ForHadronic/result/v0ttHPhasephase/eff.root', 
        #    '/eos/user/h/hhua/forTopHLT/2024H/v1ForHadronic/result/v0ttHPhasephase/eff.root', 
        #    '/eos/user/h/hhua/forTopHLT/2024I/v1ForHadronic/result/v0ttHPhasephase/eff.root', 
        # '/eos/user/h/hhua/forTopHLT/2024G/v1ForHadronic_partial/result/v0ttHPhasephase_preMD3/eff.root',
        # '/eos/user/h/hhua/forTopHLT/2024G/v1ForHadronic_partial/result/v0ttHPhasephase_postMD3/eff.root',
    # ]
    # HLT = 'HLTAll'
    # HLT = 'HH'
    legendList = []#empty list will use the era as legend
    
    
    effList = [
    #     # '/eos/home-h/hhua/forTopHLT/2024D/v1EleTTPhase/result/v0tt/eff.root',
    #     # '/eos/home-h/hhua/forTopHLT/2024E/v1EleTTPhase/result/v0tt/eff.root',
        # '/eos/home-h/hhua/forTopHLT/2024D/v1EleTTPhase/result/v1ttAndHT200/eff.root',
        # '/eos/home-h/hhua/forTopHLT/2024E/v1EleTTPhase/result/v1ttAndHT200/eff.root',
        # '/eos/user/h/hhua/forTopHLT/2024F/v1EleTTPhase/result/v1ttAndHT200/eff.root',
        # '/eos/user/h/hhua/forTopHLT/2024G/v1EleTTPhase/result/v1ttAndHT200/eff.root',
        # '/eos/user/h/hhua/forTopHLT/2024F/v1MuonTTPhase/result/v1ttAndHT200/eff.root',
        # '/eos/user/h/hhua/forTopHLT/2024G/v1EleTTPhase/result/v1ttAndHT200_preMD3/eff.root',
        # '/eos/user/h/hhua/forTopHLT/2024G/v1EleTTPhase/result/v1ttAndHT200_postMD3/eff.root',
        # '/eos/user/h/hhua/forTopHLT/2024H/v1EleTTPhase/result/v1ttAndHT200/eff.root',
        # '/eos/user/h/hhua/forTopHLT/2024I/v1EleTTPhase/result/v1ttAndHT200/eff.root',
        
        # '/eos/user/h/hhua/forTopHLT/2024D/v1MuonTTPhase/result/v1ttAndHT200/eff.root',
        # '/eos/user/h/hhua/forTopHLT/2024E/v1MuonTTPhase/result/v1ttAndHT200/eff.root',
        '/eos/user/h/hhua/forTopHLT/2024F/v1MuonTTPhase/result/v1ttAndHT200/eff.root',
        # '/eos/user/h/hhua/forTopHLT/2024G/v1MuonTTPhase/result/v1ttAndHT200/eff.root',
        # '/eos/user/h/hhua/forTopHLT/2024H/v1MuonTTPhase/result/v1ttAndHT200/eff.root',
        # '/eos/user/h/hhua/forTopHLT/2024I/v1MuonTTPhase/result/v1ttAndHT200/eff.root',
    ]
    # HLT = 'HLTbothEle'
    # HLT = 'HLTcrossEle'
    # HLT = 'HLTcrossMu'
    HLT = 'HLTbothMu'
    # legendList = ['2024G_preMD', '2024G_postMD']
    
    
    
    
    effVsEras(effList, HLT, legendList)
    # effVsEras(effList, ifHadronic)
    
    # eff_HHVsAll(effList[2])

def eff_HHVsAll(inputList):
    varList = ['HT', 'jet_6pt', 'nb']
    for iVar in varList:
        eff_hardAll = ph.getEffFromFile(inputList, [f'de_{iVar}_HLTAll', f'nu_{iVar}_HLTAll'])
        eff_HH = ph.getEffFromFile(inputList, [f'de_{iVar}_HH', f'nu_{iVar}_HH'])
        effList = [eff_hardAll, eff_HH]
        # legendList = ['Hardronic triggers', 'HH parking trigger'] 
        legendList = ['HT450+6jet+1btag || HT400+6jet+2btag || HT330+4jet+3btag', 'HT280+4jet+2btag']
    
        xmin = effList[0].GetTotalHistogram().GetXaxis().GetXmin()
        xmax = effList[0].GetTotalHistogram().GetXaxis().GetXmax()
        plotName = f'{getOutDir(inputList)}HLTEff_{iVar}_HHVsAll.png'
        ph.plotOverlay(effList, legendList, 'L1T+HLT efficiency', plotName, xmin, xmax, ['2024E'], [0, 1.1], [0.2, 0.25, 0.9, 0.5])
        

def effVsEras(inputList, HLT='HLTAll', legendList=[]):
    outDir = getOutDir(inputList[0])
   
    triggerVarMap = {
        'HLTAll': ['HT', 'jet_6pt', 'nb'],
        'HH': ['HT', 'jet_6pt', 'nb'],
        'HLTcrossEle': ['ele_1pt', 'ele_1eta', 'HT'],
        'HLTbothEle': ['ele_1pt', 'ele_1eta', 'HT'],
        'HLTcrossMu': ['muon_1pt', 'muon_1eta', 'HT'],
        'HLTbothMu': ['muon_1pt', 'muon_1eta', 'HT'],
    }
    
    # for iVar in varList:
    for iVar in triggerVarMap[HLT]:
        effList = []
        eraList = []
        for iEff in inputList:
            eff = ph.getEffFromFile(iEff, [f'de_{iVar}_{HLT}', f'nu_{iVar}_{HLT}'])
            era = uf.extract_era_from_path(iEff)
            effList.append(eff)
            eraList.append(era)
        print(effList)
        
        xmin = effList[0].GetTotalHistogram().GetXaxis().GetXmin()
        xmax = effList[0].GetTotalHistogram().GetXaxis().GetXmax()
        
        plotName =  f'{outDir}HLTEff_{iVar}_{HLT}.png'
        if not legendList:
            legendList = eraList
        ph.plotOverlay(effList, legendList,  'L1T+HLT efficiency', plotName, xmin, xmax, eraList, [0, 1.1])
    
    
    

def plotEffOverLayEle(in2023B, in2023C, in2023D, in2022):
    plotEffOverlay(in2023B, in2023C, in2023D, in2022, 'eleJet', 'ele1pt')
    plotEffOverlay(in2023B, in2023C, in2023D, in2022, 'eleHT', 'ele1pt')
    # plotEffOverlay(in2023B, in2023C, in2023D, in2022, 'singleEleJet', 'ele1pt')
    # plotEffOverlay(in2023B, in2023C, in2023D, in2022, 'singleEleHT', 'ele1pt')
        
    
def plotOverLayHard(in2023D, in2024C): 
    # plotEffOverlay(in2023D, in2024C, trigger='1btag', ifHadronic=True)
    # plotEffOverlay(in2023D, in2024C, trigger='2btag', ifHadronic=True)
    # plotEffOverlay(in2023D, in2024C, trigger='both', ifHadronic=True)
    
    # plotEffOverlay(in2023D, in2024C, '1btag', 'bjetNum', ifHadronic=True)
    # plotEffOverlay(in2023D, in2024C, '2btag', 'bjetNum', ifHadronic=True)
    # plotEffOverlay(in2023D, in2024C, 'both', 'bjetNum', ifHadronic=True)
    
    # plotEffOverlay(in2023D, in2024C, '1btag', 'HT', ifHadronic=True)
    # plotEffOverlay(in2023D, in2024C, '2btag', 'HT', ifHadronic=True)
    plotEffOverlay(in2023D, in2024C, 'both', 'HT', ifHadronic=True)
    
    
    
def plotEffOverlay(in2023D, in2024C, trigger='1btag', var = 'jetNum', ifHadronic=False):    

    if ifHadronic:
        # eff_2023B = ph.getEffFromFile(in2023B, ['de_'+var, 'nu_'+var+'_'+trigger])
        # eff_2023C = ph.getEffFromFile(in2023C, ['de_'+var, 'nu_'+var+'_'+trigger])
        eff_2023D = ph.getEffFromFile(in2023D, ['de_'+var, 'nu_'+var+'_'+trigger])
        eff_2024C = ph.getEffFromFile(in2024C, ['de_'+var, 'nu_'+var+'_'+trigger])
        xmin, xmax = ph.getXrangeFromFile(in2024C, ['de_'+var, 'nu_'+var+'_'+trigger])
    else:
        # eff_2023B = ph.getEffFromFile(in2023B, ['de_'+var+'_'+trigger, 'nu_'+var+'_'+trigger])
        # eff_2023C = ph.getEffFromFile(in2023C, ['de_'+var+'_'+trigger, 'nu_'+var+'_'+trigger])
        eff_2023D = ph.getEffFromFile(in2023D, ['de_'+var+'_'+trigger, 'nu_'+var+'_'+trigger])
        eff_2024 = ph.getEffFromFile(in2022, ['de_'+var+'_'+trigger, 'nu_'+var+'_'+trigger])
        xmin, xmax = ph.getXrangeFromFile(in2022, ['de_'+var+'_'+trigger, 'nu_'+var+'_'+trigger])
        
    histList = [eff_2024C,eff_2023D]
    #legendList = ['2024C', '2023D']
    legendList = ['2024D_preCalib', '2024D_postCalib']
    #histList = [eff_2023B, eff_2023C]
    #legendList = ['2023B', '#splitline{2023C}{#splitline{(pre HCAL}{scale change)}}']
    outDir = getOutDir(in2024C) 
    plotName = outDir + 'HLTEff_'+var+'_'+trigger+'.png'
    ph.plotOverlay(histList, legendList, '2023', 'L1T+HLT efficiency', plotName, xmin, xmax, [0, 1.1])
   

 
    

 
   
    
def getOutDir(inputFile):
    inputDir = inputFile.rsplit('/', 1)[0] +'/'
    outDir = inputDir+'results/'
    if not os.path.exists(outDir):
        os.makedirs(outDir)
    return outDir
     
    
        
    
if __name__=='__main__':
    main() 
    
