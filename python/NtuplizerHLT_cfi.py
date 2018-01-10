import FWCore.ParameterSet.Config as cms

TFileService = cms.Service("TFileService",
	fileName = cms.string('ntuple.root')
)

from Analysis.Ntuplizer.MssmHbbNtuplizerTriggerPathsHLT_cfi import *
from Analysis.Ntuplizer.MssmHbbNtuplizerL1SeedsHLT_cfi import *
from Analysis.Ntuplizer.MssmHbbNtuplizerBtagHLT_cfi import *
from Analysis.Ntuplizer.MssmHbbNtuplizerTriggerEventHLT_cfi import *


## ============  THE NTUPLIZER!!!  ===============
ntuplizer           = cms.EDAnalyzer("Ntuplizer",
    # Imported settings (always at the beginning)
    MssmHbbNtuplizerBtagHLT,
    MssmHbbNtuplizerTriggerPathsHLT,
    MssmHbbNtuplizerL1SeedsHLT,
    MssmHbbNtuplizerTriggerEventHLT,
    MonteCarlo      = cms.bool(False),
    ## Monte Carlo only
#     GenFilterInfo   = cms.InputTag("genFilterEfficiencyProducer"),
#     GenRunInfo      = cms.InputTag("generator"),
#     GenEventInfo    = cms.InputTag("generator"),
#     PileupInfo      = cms.InputTag("addPileupInfo","","HLT"),
    ###################
    TotalEvents     = cms.InputTag ('TotalEvents'),
    FilteredEvents  = cms.InputTag ('FilteredEvents'),
    PatJets         = cms.VInputTag( cms.InputTag('slimmedJets'), cms.InputTag('slimmedJetsPuppi') ),
#    FixedGridRhoAll = cms.InputTag ('fixedGridRhoAll'),
    PatMuons        = cms.VInputTag(cms.InputTag('slimmedMuons') ), 
    PrimaryVertices = cms.VInputTag(cms.InputTag('offlineSlimmedPrimaryVertices') ),
    TriggerResults  = cms.VInputTag(cms.InputTag('TriggerResults','','HLT') ),
    L1TJets         = cms.VInputTag(cms.InputTag('caloStage2Digis','Jet','RECO'), ),
    L1TMuons        = cms.VInputTag(cms.InputTag('gmtStage2Digis','Muon','RECO'), ),
    TriggerEvent    = cms.VInputTag(cms.InputTag('hltTriggerSummaryAOD','','HLT'), ),
)
