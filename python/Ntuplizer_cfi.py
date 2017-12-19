import FWCore.ParameterSet.Config as cms

TFileService = cms.Service("TFileService",
	fileName = cms.string('ntuple.root')
)

from Analysis.Ntuplizer.MssmHbbNtuplizerTriggerPaths_cfi import *
from Analysis.Ntuplizer.MssmHbbNtuplizerL1Seeds_cfi import *
from Analysis.Ntuplizer.MssmHbbNtuplizerTriggerObjects_cfi import *
from Analysis.Ntuplizer.MssmHbbNtuplizerBtag_cfi import *


## ============  THE NTUPLIZER!!!  ===============
ntuplizer           = cms.EDAnalyzer("Ntuplizer",
    # Imported settings (always at the beginning)
    MssmHbbNtuplizerBtag,
    MssmHbbNtuplizerTriggerPaths,
    MssmHbbNtuplizerL1Seeds,
    MssmHbbNtuplizerTriggerObjects,
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
    TriggerObjectStandAlone = cms.VInputTag(cms.InputTag('slimmedPatTrigger'), ),
)
