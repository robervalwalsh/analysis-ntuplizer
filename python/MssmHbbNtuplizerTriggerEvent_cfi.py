import FWCore.ParameterSet.Config as cms

MssmHbbNtuplizerTriggerEvent = cms.PSet(
   TriggerObjectLabels    = cms.vstring  (
                                             'hltL1sZeroBias',
                                             'hltSingleCaloJet10',
                                             'hltSinglePFJet40',
                                             
                                             'hltL1sSingleMu3IorSingleMu5IorSingleMu7',
                                             'hltL1fL1sMu5L1Filtered0',
                                             'hltL3fL1sMu5L1f0L2f5L3Filtered8',
   ),
)
