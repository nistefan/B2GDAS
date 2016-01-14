#! /usr/bin/env python

1
## _________                _____.__                            __  .__               
## \_   ___ \  ____   _____/ ____\__| ____  __ ______________ _/  |_|__| ____   ____  
## /    \  \/ /  _ \ /    \   __\|  |/ ___\|  |  \_  __ \__  \\   __\  |/  _ \ /    \ 
## \     \___(  <_> )   |  \  |  |  / /_/  >  |  /|  | \// __ \|  | |  (  <_> )   |  \
##  \______  /\____/|___|  /__|  |__\___  /|____/ |__|  (____  /__| |__|\____/|___|  /
##         \/            \/        /_____/                   \/                    \/ 
import sys
import math
import array as array
from optparse import OptionParser
from math import sqrt


def plot_mttbar(argv) : 
    parser = OptionParser()

    parser.add_option('--file_in', type='string', action='store',
                      dest='file_in',
                      help='Input file')

    parser.add_option('--file_out', type='string', action='store',
                      dest='file_out',
                      help='Output file')
    
    parser.add_option('--isData', action='store_true',
                      dest='isData',
                      default = False,
                      help='Is this Data?')

    parser.add_option('--isElectron', action='store_true',
                      dest='isElectron',
                      default = False,
                      help='Is Electron?')
        
    (options, args) = parser.parse_args(argv)
    argv = []

    print '===== Command line options ====='
    print options
    print '================================'

    import ROOT

    btag_sf_func = ROOT.TF1("btag_sf", "-(0.0443172)+(0.00496634*(log(x+1267.85)*(log(x+1267.85)*(3-(-(0.110428*log(x+1267.85)))))))")

    from leptonic_nu_z_component import solve_nu_tmass, solve_nu

    fout= ROOT.TFile.Open(options.file_out, "RECREATE")
    h_mttbar = ROOT.TH1F("h_mttbar", ";m_{t#bar{t}} (GeV);Number", 100, 0, 5000)
    h_mtopHad = ROOT.TH1F("h_mtopHad", ";m_{jet} (GeV);Number", 100, 0, 400)
    h_mtopHadGroomed = ROOT.TH1F("h_mtopHadGroomed", ";Groomed m_{jet} (GeV);Number", 100, 0, 400)
    h_mttbarCorrectedUp = ROOT.TH1F("h_mtopHadCorrectedUp", ";mtopHad Corrected Up;Number", 100, 0, 5000)
    h_mttbarCorrectedDown = ROOT.TH1F("h_mtopHadCorrectedDown", ";mtopHad Corrected Down;Number", 100, 0, 5000)
    h_mttbarCorrectedUpRES = ROOT.TH1F("h_mtopHadCorrectedUpRES", ";mtopHad Corrected Up Res;Number", 100, 0, 5000)
    h_mttbarCorrectedDownRES = ROOT.TH1F("h_mtopHadCorrectedDownRES", ";mtopHad Corrected Down Res;Number", 100, 0, 5000)
    
    #Histgrams before Cuts
    h_mttbar_pre               = ROOT.TH1F("h_mttbar_pre", ";m_{t#bar{t}} (GeV);Number", 100, 0, 5000)
    h_mtopHad_pre              = ROOT.TH1F("h_mtopHad_pre", ";m_{jet} (GeV);Number", 100, 0, 400)
    h_2D_pre                   = ROOT.TH2F('2D_cut_pre',";Pt Real; DeltaR",100,0,400,40,-4,4)
    h_FatJetPt_pre             = ROOT.TH1F('h_FatJetPt_pre',"; AK8Jet Pt (GeV);Number",100,0,4000)
    h_FatJetRapidity_pre       = ROOT.TH1F(' h_FatJetRapidity_pre',"; AK8Jet Rapidity ;Number",100,-4,4)
    h_FatJetPhi_pre            = ROOT.TH1F(' h_FatJetPhi_pre',"; AK8Jet Phi ;Number",100,-4,4)
    h_FatJetMass_pre           = ROOT.TH1F('h_FatJetMass_pre',"; AK8Jet Mass (GeV);Number",100,0,400)
    h_FatJetMassSoftDrop_pre   = ROOT.TH1F('h_FatJetMassSoftDrop_pre',"; AK8Jet Mass SoftDrop (GeV);Number",100,0,400)
    h_FatJetTau32_pre          = ROOT.TH1F('h_FatJetTau32_pre',"AK8Jet Tau32;Number",100,0,1)
    h_LeptonPt_pre             = ROOT.TH1F('h_LeptonPt_pre',"; Lepton Pt (GeV);Number",100,0,400)
    h_LeptonPseudoRapidity_pre = ROOT.TH1F('h_LeptonPseudoRapidity_pre',"; Lepton PseudoRapidity;Number",100,-4,4)
    h_LeptonPhi_pre            = ROOT.TH1F(' h_LeptonPhi_pre',"; Lepton Phi ;Number",100,-4,4)
    h_NearestAK4JetPt_pre      = ROOT.TH1F('h_NearestAK4JetPt_pre',"; NearAK4Jet Pt (GeV);Number",100,0,2000)
    h_NearestAK4JetRapidity_pre= ROOT.TH1F('h_NearestAK4JeRapidity_pre',"; NearAK4Jet Rapidity ;Number",100,-4,4)
    h_NearestAK4JetPhi_pre     = ROOT.TH1F('h_NearestAK4JePhi_pre',"; NearAK4Jet Phi ;Number",100,-4,4)
    h_NearestAK4JetMass_pre    = ROOT.TH1F('h_NearestAK4JetMass_pre',"; NearAK4Jet Mass (GeV);Number",100,0,400)
    h_AK4bDisc_pre             = ROOT.TH1F('h_AK4bDisc_pre',"AK4Jet bDisc;Number",100,0,1)
    h_MissingEt_pre            = ROOT.TH1F('h_MissingET_pre',"Missing ET (GeV);Number",100,0,400)
    h_LeptonHt_pre             = ROOT.TH1F('h_LeptonHt_pre',"Lepton Ht (GeV);Number",100,0,500)
    
    #adding histgram after Cuts
    h_2D                     = ROOT.TH2F('2D_cut',";Pt Real; DeltaR",100,0,400,40,-4,4)
    h_FatJetPt               = ROOT.TH1F('h_FatJetPt',"; AK8Jet Pt (GeV);Number",100,0,4000)
    h_FatJetRapidity         = ROOT.TH1F(' h_FatJetRapidity',"; AK8Jet Rapidity ;Number",100,-4,4)
    h_FatJetPhi              = ROOT.TH1F(' h_FatJetPhi',"; AK8Jet Phi ;Number",100,-4,4)
    h_FatJetMass             = ROOT.TH1F('h_FatJetMass',"; AK8Jet Mass (GeV);Number",100,0,400)
    h_FatJetMassSoftDrop     = ROOT.TH1F('h_FatJetMassSoftDrop',"; AK8Jet Mass SoftDrop (GeV);Number",100,0,400)
    h_FatJetTau32            = ROOT.TH1F('h_FatJetTau32',"AK8Jet Tau32;Number",100,0,1)
    h_LeptonPt               = ROOT.TH1F('h_LeptonPt',"; Lepton Pt (GeV);Number",100,0,400)
    h_LeptonPseudoRapidity   = ROOT.TH1F('h_LeptonPseudoRapidity',"; Lepton PseudoRapidity;Number",100,-4,4)
    h_LeptonPhi              = ROOT.TH1F(' h_LeptonPhi',"; Lepton Phi ;Number",100,-4,4)
    h_NearestAK4JetPt        = ROOT.TH1F('h_NearestAK4JetPt',"; NearAK4Jet Pt (GeV);Number",100,0,2000)
    h_NearestAK4JetRapidity  = ROOT.TH1F('h_NearestAK4JeRapidity',"; NearAK4Jet Rapidity ;Number",100,-4,4)
    h_NearestAK4JetPhi       = ROOT.TH1F('h_NearestAK4JePhi',"; NearAK4Jet Phi ;Number",100,-4,4)
    h_NearestAK4JetMass      = ROOT.TH1F('h_NearestAK4JetMass',"; NearAK4Jet Mass (GeV);Number",100,0,400)
    h_AK4bDisc               = ROOT.TH1F('h_AK4bDisc',"AK4Jet bDisc;Number",100,0,1)
    h_MissingEt              = ROOT.TH1F('h_MissingET',"Missing ET (GeV);Number",100,0,400)
    h_LeptonHt               = ROOT.TH1F('h_LeptonHt',"Lepton Ht (GeV);Number",100,0,500)

    fin = ROOT.TFile.Open(options.file_in)
    Npre = 0.
    Nnum = 0.

    trees = [ fin.Get("TreeSemiLept") ]

    EventRunNum = 0
    EventLumiBlock = 0
    EventNum = 0
    Mttbar = 0 
    
    for itree,t in enumerate(trees) :

        if options.isData : 
            SemiLeptTrig        = array.array('i', [0]  )
        SemiLeptWeight      = array.array('f', [0.] )
        PUWeight            = array.array('f', [0.] )
        GenWeight           = array.array('f', [0.] )
        FatJetPt            = array.array('f', [-1.])
        FatJetEta           = array.array('f', [-1.])
        FatJetPhi           = array.array('f', [-1.])
        FatJetRap           = array.array('f', [-1.])
        FatJetEnergy        = array.array('f', [-1.])
        FatJetBDisc         = array.array('f', [-1.])
        FatJetMass          = array.array('f', [-1.])
        FatJetMassSoftDrop  = array.array('f', [-1.])
        FatJetTau32         = array.array('f', [-1.])
        FatJetTau21         = array.array('f', [-1.]) 
        FatJetSDbdiscW      = array.array('f', [-1.])
        FatJetSDbdiscB      = array.array('f', [-1.])
        FatJetSDsubjetWpt   = array.array('f', [-1.])
        FatJetSDsubjetWmass = array.array('f', [-1.])
        FatJetSDsubjetBpt   = array.array('f', [-1.])
        FatJetSDsubjetBmass = array.array('f', [-1.])
        FatJetJECUpSys      = array.array('f', [-1.])
        FatJetJECDnSys      = array.array('f', [-1.])
        FatJetJERUpSys      = array.array('f', [-1.])
        FatJetJERDnSys      = array.array('f', [-1.])
        LeptonType          = array.array('i', [-1])
        LeptonPt            = array.array('f', [-1.])
        LeptonEta           = array.array('f', [-1.])
        LeptonPhi           = array.array('f', [-1.])
        LeptonEnergy        = array.array('f', [-1.])
        LeptonIso           = array.array('f', [-1.])
        LeptonPtRel         = array.array('f', [-1.])
        LeptonDRMin         = array.array('f', [-1.])
        SemiLepMETpt        = array.array('f', [-1.])
        SemiLepMETphi       = array.array('f', [-1.])
        SemiLepNvtx         = array.array('f', [-1.])
        DeltaPhiLepFat      = array.array('f', [-1.]) 
        AK4bDisc            = array.array('f', [-1.])
        NearestAK4JetPt     = array.array('f', [-1.])
        NearestAK4JetEta    = array.array('f', [-1.])
        NearestAK4JetPhi    = array.array('f', [-1.])
        NearestAK4JetMass   = array.array('f', [-1.])
        NearestAK4JetJECUpSys = array.array('f', [-1.])
        NearestAK4JetJECDnSys = array.array('f', [-1.])
        NearestAK4JetJERUpSys = array.array('f', [-1.])
        NearestAK4JetJERDnSys = array.array('f', [-1.])
        SemiLeptRunNum        = array.array('f', [-1.])   
        SemiLeptLumiBlock     = array.array('f', [-1.])   
        SemiLeptEventNum      = array.array('f', [-1.])   



        if options.isData : 
            t.SetBranchAddress('SemiLeptTrig'        , SemiLeptTrig        )
        t.SetBranchAddress('SemiLeptWeight'      , SemiLeptWeight      )
        t.SetBranchAddress('PUWeight'            , PUWeight            )
        t.SetBranchAddress('GenWeight'           , GenWeight               )
        t.SetBranchAddress('FatJetPt'            , FatJetPt            )
        t.SetBranchAddress('FatJetEta'           , FatJetEta           )
        t.SetBranchAddress('FatJetPhi'           , FatJetPhi           )
        t.SetBranchAddress('FatJetRap'           , FatJetRap           )
        t.SetBranchAddress('FatJetEnergy'        , FatJetEnergy        )
        t.SetBranchAddress('FatJetBDisc'         , FatJetBDisc         )
        t.SetBranchAddress('FatJetMass'          , FatJetMass           )
        t.SetBranchAddress('FatJetMassSoftDrop'  , FatJetMassSoftDrop  )
        t.SetBranchAddress('FatJetTau32'         , FatJetTau32         )
        t.SetBranchAddress('FatJetTau21'         , FatJetTau21         )
        t.SetBranchAddress('FatJetSDbdiscW'      , FatJetSDbdiscW      )
        t.SetBranchAddress('FatJetSDbdiscB'      , FatJetSDbdiscB              )
        t.SetBranchAddress('FatJetSDsubjetWpt'   , FatJetSDsubjetWpt   )
        t.SetBranchAddress('FatJetSDsubjetWmass' , FatJetSDsubjetWmass )
        t.SetBranchAddress('FatJetSDsubjetBpt'   , FatJetSDsubjetBpt   )
        t.SetBranchAddress('FatJetSDsubjetBmass' , FatJetSDsubjetBmass )
        t.SetBranchAddress('FatJetJECUpSys'      , FatJetJECUpSys      )
        t.SetBranchAddress('FatJetJECDnSys'      , FatJetJECDnSys      )
        t.SetBranchAddress('FatJetJERUpSys'      , FatJetJERUpSys      )
        t.SetBranchAddress('FatJetJERDnSys'      , FatJetJERDnSys      )
        t.SetBranchAddress('LeptonType'          , LeptonType          )
        t.SetBranchAddress('LeptonPt'            , LeptonPt            )
        t.SetBranchAddress('LeptonEta'           , LeptonEta           )
        t.SetBranchAddress('LeptonPhi'           , LeptonPhi           )
        t.SetBranchAddress('LeptonEnergy'        , LeptonEnergy        )
        t.SetBranchAddress('LeptonIso'           , LeptonIso           )
        t.SetBranchAddress('LeptonPtRel'         , LeptonPtRel         )
        t.SetBranchAddress('LeptonDRMin'         , LeptonDRMin         )
        t.SetBranchAddress('SemiLepMETpt'        , SemiLepMETpt        )
        t.SetBranchAddress('SemiLepMETphi'       , SemiLepMETphi       )
        t.SetBranchAddress('SemiLepNvtx'         , SemiLepNvtx         )
        t.SetBranchAddress('DeltaPhiLepFat'      , DeltaPhiLepFat      )
        t.SetBranchAddress('AK4bDisc'            ,AK4bDisc             )
        t.SetBranchAddress('NearestAK4JetPt'     ,NearestAK4JetPt      )
        t.SetBranchAddress('NearestAK4JetEta'    ,NearestAK4JetEta     )
        t.SetBranchAddress('NearestAK4JetPhi'    ,NearestAK4JetPhi     )
        t.SetBranchAddress('NearestAK4JetMass'   ,NearestAK4JetMass    )
        t.SetBranchAddress('NearestAK4JetJECUpSys'      , NearestAK4JetJECUpSys)
        t.SetBranchAddress('NearestAK4JetJECDnSys'      , NearestAK4JetJECDnSys)
        t.SetBranchAddress('NearestAK4JetJERUpSys'      , NearestAK4JetJERUpSys)
        t.SetBranchAddress('NearestAK4JetJERDnSys'      , NearestAK4JetJERDnSys)
        t.SetBranchAddress('SemiLeptRunNum'         ,  SemiLeptRunNum       )
        t.SetBranchAddress('SemiLeptLumiBlock'      ,  SemiLeptLumiBlock    )
        t.SetBranchAddress('SemiLeptEventNum'       ,  SemiLeptEventNum     )


        t.SetBranchStatus ('*', 0)
        t.SetBranchStatus ('PUWeight', 1)
        t.SetBranchStatus ('FatJetPt', 1)
        t.SetBranchStatus ('FatJetEta', 1)
        t.SetBranchStatus ('FatJetPhi', 1)
        t.SetBranchStatus ('FatJetMass', 1)
        t.SetBranchStatus ('FatJetMassSoftDrop', 1)
        t.SetBranchStatus ('FatJetTau32', 1)
        t.SetBranchStatus ('SemiLeptTrig', 1)
        t.SetBranchStatus ('AK4bDisc', 1)
        t.SetBranchStatus ('NearestAK4JetPt'   ,1 )
        t.SetBranchStatus ('NearestAK4JetEta'  ,1 )
        t.SetBranchStatus ('NearestAK4JetPhi'  ,1 )
        t.SetBranchStatus ('NearestAK4JetMass' ,1 )
        t.SetBranchStatus ('SemiLepMETpt' , 1 )
        t.SetBranchStatus ('SemiLepMETphi' , 1 )
        t.SetBranchStatus ('LeptonType'          , 1 )
        t.SetBranchStatus ('LeptonPt'            , 1)
        t.SetBranchStatus ('LeptonEta'           , 1)
        t.SetBranchStatus ('LeptonPhi'           , 1)
        t.SetBranchStatus ('LeptonEnergy'        , 1)
        t.SetBranchStatus ('LeptonIso'           , 1)
        t.SetBranchStatus ('LeptonPtRel'         , 1)
        t.SetBranchStatus ('LeptonDRMin'         , 1)
        t.SetBranchStatus ('FatJetJECUpSys'         , 1)
        t.SetBranchStatus ('FatJetJECDnSys'         , 1)
        t.SetBranchStatus ('FatJetJERUpSys'         , 1)
        t.SetBranchStatus ('FatJetJERDnSys'         , 1)
        t.SetBranchStatus ('SemiLeptRunNum'         , 1)
        t.SetBranchStatus ('SemiLeptLumiBlock'      , 1)
        t.SetBranchStatus ('SemiLeptEventNum'       , 1)
        # set the Trig and lepton Type for electron and Muon
        if options.isElectron:
            TrigCheck = 6
            LeptonTypeCheck =11
        else :
            TrigCheck = 3
            LeptonTypeCheck =13

        entries = t.GetEntriesFast()
        print 'Processing tree ' + str(itree)

        eventsToRun = entries
        for jentry in xrange( eventsToRun ):
            if jentry % 100000 == 0 :
                print 'processing ' + str(jentry)
            # get the next tree in the chain and verify
            ientry = t.GetEntry( jentry )

            if ientry < 0: 
                break
            
            # check the event is Muon or Electron and skip the event that not Muon and Electron 
            if (options.isData and SemiLeptTrig[0]!= TrigCheck) or (LeptonType[0] !=LeptonTypeCheck) :
                continue 


            hadTopCandP4 = ROOT.TLorentzVector()
            hadTopCandP4Corrected = ROOT.TLorentzVector()
            hadTopCandP4.SetPtEtaPhiM( FatJetPt[0], FatJetEta[0], FatJetPhi[0], FatJetMass[0])
            bJetCandP4 = ROOT.TLorentzVector()
            bJetCandP4.SetPtEtaPhiM( NearestAK4JetPt[0], NearestAK4JetEta[0], NearestAK4JetPhi[0], NearestAK4JetMass[0])
            nuCandP4 = ROOT.TLorentzVector( )
            nuCandP4.SetPtEtaPhiM( SemiLepMETpt[0], 0, SemiLepMETphi[0], SemiLepMETpt[0] )
            theLepton = ROOT.TLorentzVector()
            theLepton.SetPtEtaPhiE( LeptonPt[0], LeptonEta[0], LeptonPhi[0], LeptonEnergy[0] ) # Assume massless
            
            # JEC and JER
            hadTopCandP4CorrectedUp = hadTopCandP4 * FatJetJECUpSys[0]
            hadTopCandP4CorrectedDown = hadTopCandP4 * FatJetJECDnSys[0]
            hadTopCandP4CorrectedUpRES = hadTopCandP4 * FatJetJERUpSys[0]
            hadTopCandP4CorrectedDownRES = hadTopCandP4 * FatJetJERDnSys[0]

            #print FatJetJECUpSys[0] , '/////' , FatJetJERUpSys[0]

            #print hadTopCandP4Corrected[1]
            tau32 = FatJetTau32[0]
            mass_sd = FatJetMassSoftDrop[0]
            bdisc = AK4bDisc[0]
        
            passKin = hadTopCandP4.Perp() > 400.
            passTopTag = tau32 < 0.6 and mass_sd > 110. and mass_sd < 210.
            pass2DCut = LeptonPtRel[0] > 55. or LeptonDRMin[0] > 0.4
            passBtag = bdisc > 0.7
            
            passNpre = passKin and pass2DCut and hadTopCandP4.Perp() > 400 and  mass_sd > 90 and abs(FatJetEta[0])< 2.4

            passNnum = passNpre and mass_sd > 110 and mass_sd < 210 and tau32 < 0.6

            if passNpre :
                Npre += 1 #PUWeight[0]

                if passNnum :
                    Nnum += 1 #PUWeight[0]
             
                
            ##  ____  __.__                              __  .__         __________                     
            ## |    |/ _|__| ____   ____   _____ _____ _/  |_|__| ____   \______   \ ____   ____  ____  
            ## |      < |  |/    \_/ __ \ /     \\__  \\   __\  |/ ___\   |       _// __ \_/ ___\/  _ \ 
            ## |    |  \|  |   |  \  ___/|  Y Y  \/ __ \|  | |  \  \___   |    |   \  ___/\  \__(  <_> )
            ## |____|__ \__|___|  /\___  >__|_|  (____  /__| |__|\___  >  |____|_  /\___  >\___  >____/ 
            ##         \/       \/     \/      \/     \/             \/          \/     \/     \/       

            # Now we do our kinematic calculation based on the categories of the
            # number of top and bottom tags
            mttbar = -1.0


            lepTopCandP4 = None
            # Get the z-component of the lepton from the W mass constraint
            solution, nuz1, nuz2 = solve_nu( vlep=theLepton, vnu=nuCandP4 )
            # If there is at least one real solution, pick it up
            if solution :
                nuCandP4.SetPz( nuz1 )
            else :
                nuCandP4.SetPz( nuz1.real )

            lepTopCandP4 = nuCandP4 + theLepton + bJetCandP4

            ttbarCand = hadTopCandP4 + lepTopCandP4
            ttbarCandUp = hadTopCandP4CorrectedUp + lepTopCandP4
            ttbarCandDown = hadTopCandP4CorrectedDown + lepTopCandP4
            ttbarCandUpRES = hadTopCandP4CorrectedUpRES + lepTopCandP4
            ttbarCandDownRES = hadTopCandP4CorrectedDownRES + lepTopCandP4
            mttbar = ttbarCand.M()

            weight = PUWeight[0]* btag_sf_func.Eval(NearestAK4JetPt[0])
            
            if options.isData : 
                weight =1 


            mttbarUp = ttbarCandUp.M()
            mttbarDown = ttbarCandDownRES.M()
            mttbarUpRES = ttbarCandUpRES.M()
            mttbarDownRES = ttbarCandDown.M()
               
            #Adding Histgrams before Cuts
               
            h_2D_pre.Fill( LeptonPtRel[0] , LeptonDRMin[0], weight)
            h_mttbar_pre.Fill( mttbar, weight )
            h_mtopHad_pre.Fill( hadTopCandP4.M(), weight )
            h_FatJetPt_pre.Fill(hadTopCandP4.Pt(),weight)
            h_FatJetRapidity_pre.Fill(hadTopCandP4.Rapidity(),weight)
            h_FatJetPhi_pre.Fill(hadTopCandP4.Phi(),weight)
            h_FatJetMass_pre.Fill(hadTopCandP4.M(),weight)
            h_FatJetMassSoftDrop_pre.Fill(mass_sd,weight) 
            h_FatJetTau32_pre.Fill(tau32,weight)
            h_LeptonPt_pre.Fill(theLepton.Pt(),weight)
            h_LeptonPseudoRapidity_pre.Fill(theLepton.PseudoRapidity(),weight)
            h_LeptonPhi_pre.Fill(theLepton.Phi(),weight)
            h_NearestAK4JetPt_pre.Fill(bJetCandP4.Pt(),weight)
            h_NearestAK4JetRapidity_pre.Fill(bJetCandP4.Rapidity(),weight)
            h_NearestAK4JetPhi_pre.Fill(bJetCandP4.Phi(),weight)
            h_NearestAK4JetMass_pre.Fill(bJetCandP4.M(),weight)
            h_AK4bDisc_pre.Fill(bdisc,weight)
            h_MissingEt_pre.Fill(nuCandP4.Perp(),weight)
            h_LeptonHt_pre.Fill(nuCandP4.Perp()+theLepton.Pt(),weight)


            
            #### applying cuts
           
            if not passKin or not pass2DCut or not passBtag or not passTopTag :
                continue


          
            h_mttbarCorrectedUp.Fill( mttbarUp, weight )
            h_mttbarCorrectedDown.Fill( mttbarDown, weight )

            h_mttbarCorrectedUpRES.Fill( mttbarUpRES , weight )
            h_mttbarCorrectedDownRES.Fill( mttbarDownRES , weight )


             
           
            h_2D.Fill( LeptonPtRel[0] , LeptonDRMin[0], weight)
            h_mttbar.Fill( mttbar, weight )
            h_mtopHad.Fill( hadTopCandP4.M(), weight )
            h_FatJetPt.Fill(hadTopCandP4.Pt(),weight)
            h_FatJetRapidity.Fill(hadTopCandP4.Rapidity(),weight)
            h_FatJetPhi.Fill(hadTopCandP4.Phi(),weight)
            h_FatJetMass.Fill(hadTopCandP4.M(),weight)
            h_FatJetMassSoftDrop.Fill(mass_sd,weight) 
            h_FatJetTau32.Fill(tau32,weight)
            h_LeptonPt.Fill(theLepton.Pt(),weight)
            h_LeptonPseudoRapidity.Fill(theLepton.PseudoRapidity(),weight)
            h_LeptonPhi.Fill(theLepton.Phi(),weight)
            h_NearestAK4JetPt.Fill(bJetCandP4.Pt(),weight)
            h_NearestAK4JetRapidity.Fill(bJetCandP4.Rapidity(),weight)
            h_NearestAK4JetPhi.Fill(bJetCandP4.Phi(),weight)
            h_NearestAK4JetMass.Fill(bJetCandP4.M(),weight)
            h_AK4bDisc.Fill(bdisc,weight)
            h_MissingEt.Fill(nuCandP4.Perp(),weight)
            h_LeptonHt.Fill(nuCandP4.Perp()+theLepton.Pt(),weight)
            #print the large mass event ID 
            if mttbar > 2000 :
                EventRunNum = SemiLeptRunNum[0]
                EventLumiBlock = SemiLeptLumiBlock[0]
                EventNum = SemiLeptEventNum[0]
                print "Event Run Number", EventRunNum,"Event Lumi Block" ,EventLumiBlock,"Event Number", EventNum, "Mass of ttbar" ,mttbar
            
        uncibin =0     
        xnbins = h_mtopHad.GetXaxis().GetNbins()
        for ibin in xrange( xnbins ):
            val =  h_mttbar.GetBinContent(ibin)
            valup = h_mttbarCorrectedUp.GetBinContent(ibin)
            valdown = h_mttbarCorrectedDown.GetBinContent(ibin)
            jesup = abs(valup - val)
            jesdown = abs(valdown - val)
            jesun = 0.5 * ( jesup + jesdown)
            if val!= 0 :
                uncibin = h_mttbar.GetBinContent(ibin)/val
            unc = sqrt(pow(jesun,2)+pow(uncibin,2))
            h_mttbar.SetBinError(ibin, unc*val)
            
        
                
            
    Eff = Nnum/Npre
    dEff = math.sqrt( Eff * (1.0-Eff) / Npre )
    print Nnum, Npre, Eff, dEff
  #  print "Event Run Number", EventRunNum,"Event Lumi Block" ,EventLumiBlock,"Event Number", EventNum, "Mass of ttbar" ,Mttbar

    fout.cd()
    fout.Write()
    fout.Close()

if __name__ == "__main__" :
    plot_mttbar(sys.argv)


