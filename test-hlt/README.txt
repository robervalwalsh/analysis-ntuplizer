### how to include ntuplizer (+ filters) within cmsDriver config
### cmsDriver commands

#_______________________________________________________________

# include ntuplizer (+ filters) within cmsDriver config
#_______________ Addition to cmsDriver - begin

# pileup filter MC
process.RemovePileUpDominatedEventsGen = cms.EDFilter("RemovePileUpDominatedEventsGen")

# Trigger filter (HLT config)
from Analysis.Ntuplizer.TriggerFilter_cfi import triggerFilter

# =========================
# Trigger config modifications
# Example triggers
#                                  'HLT_BTagMu_DiJet20_Mu5_v*',
#                                  'HLT_ZeroBias_BunchTrains_part*',
#                                  'HLT_ZeroBias_part0_v*',
process.triggerFilter = triggerFilter.clone()
process.triggerFilter.hltResults = cms.InputTag( 'TriggerResults', '', 'HLT' )
process.triggerFilter.triggerConditions  = cms.vstring  (
                                  'HLT_ZeroBias_BunchTrains_part*',
                                  )
# comment or modified the lines below if no filter or other filters are required
process.HLTBeginSequence.insert(-1,process.triggerFilter)                    # data
#process.HLTBeginSequence.insert(-1,process.RemovePileUpDominatedEventsGen)   # qcd MC
# =========================

# Trigger filter (this config)
process.localFilter = triggerFilter.clone()
process.localFilter.hltResults = cms.InputTag( 'TriggerResults', '', 'HLT2' )
process.localFilter.triggerConditions  = cms.vstring  (
                                  'HLT_CaloJets_Muons_CaloBTagCSV_PFJets_v*',
                                  )

# Ntuplizer
from Analysis.Ntuplizer.Ntuplizer_cfi import TFileService
process.TFileService = TFileService.clone()

from Analysis.Ntuplizer.Ntuplizer_cfi import ntuplizer
process.MssmHbbTrigger = ntuplizer.clone()
process.MssmHbbTrigger.MonteCarlo        = cms.bool(False)
process.MssmHbbTrigger.JetsTags          = cms.VInputTag(cms.InputTag('hltCombinedSecondaryVertexBJetTagsCalo'))
process.MssmHbbTrigger.L1TJets           = cms.VInputTag(cms.InputTag('hltCaloStage2Digis','Jet'))
process.MssmHbbTrigger.L1TMuons          = cms.VInputTag(cms.InputTag('hltGmtStage2Digis','Muon'))
process.MssmHbbTrigger.ChargedCandidates = cms.VInputTag(cms.InputTag('hltL2MuonCandidates'),cms.InputTag('hltL3MuonCandidates') )
process.MssmHbbTrigger.CaloJets          = cms.VInputTag(cms.InputTag('hltAK4CaloJetsCorrectedIDPassed') )
process.MssmHbbTrigger.PFJets            = cms.VInputTag(cms.InputTag('hltAK4PFJets'),cms.InputTag('hltAK4PFJetsLooseIDCorrected'),cms.InputTag('hltAK4PFJetsTightIDCorrected'))
process.MssmHbbTrigger.TriggerResults    = cms.VInputTag(cms.InputTag('TriggerResults','','HLT2'))
process.MssmHbbTrigger.TriggerPaths      = cms.vstring ('HLT_CaloJets_Muons_CaloBTagCSV_PFJets_v')
# MC specific
#process.MssmHbbTrigger.PileupInfo        = cms.InputTag("addPileupInfo","","HLT"),
#process.MssmHbbTrigger.GenFilterInfo     = cms.InputTag("genFilterEfficiencyProducer"),
#process.MssmHbbTrigger.GenRunInfo        = cms.InputTag("generator"),                  

process.Ntuplizer = cms.Sequence(process.localFilter + process.MssmHbbTrigger)
process.ntuplizer_step = cms.EndPath(process.Ntuplizer)

#_______________ Addition to cmsDriver - end

...
process.schedule.extend([process.endjob_step,process.ntuplizer_step]) # Modified wrt cmsDriver 

#_______________________________________________________________

# cmsDriver commands

 DATA
======

cmsDriver.py step2 \
--step=L1REPACK:Full,HLT:User80Xv35 \
--conditions=auto:run2_hlt_GRun \
--filein=/store/data/Run2016H/BTagMu/RAW/v1/000/283/408/00000/78879B75-CC94-E611-BAE6-02163E0146EA.root \
--custom_conditions= \
--number=10 \
--data \
--no_exec \
--datatier RAW\
--eventcontent=RAW\
--customise=HLTrigger/Configuration/CustomConfigs.L1THLT \
--era=Run2_2016 \
--customise= \
--scenario=pp \
--python_filename=ReHLT_L1Trepack_HLTUser80Xv35_DataNtuple.py \
--processName=HLT2 \
--no_output


 MC
====

cmsDriver.py step2 \
--step=L1REPACK:FullMC,HLT:User80Xv35 \
--conditions=auto:run2_mc_GRun \
--filein=/store/mc/RunIISummer16DR80/QCD_Pt_15to30_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/110000/021D009D-21A3-E611-B83B-0025905A6080.root \
--secondfilein= \
--custom_conditions= \
--number=100 \
--mc\
--no_exec \
--datatier RAW\
--eventcontent=RAW\
--customise=HLTrigger/Configuration/CustomConfigs.L1THLT \
--era=Run2_2016 \
--customise= \
--scenario=pp \
--python_filename=ReHLT_L1Trepack_HLTUser80Xv35_MCNtuple.py \
--processName=HLT2 \
--no_output
