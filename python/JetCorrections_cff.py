import FWCore.ParameterSet.Config as cms

from  PhysicsTools.PatAlgos.recoLayer0.jetCorrFactors_cfi import *
# Note: Safe to always add 'L2L3Residual' as MC contains dummy L2L3Residual corrections (always set to 1)
#      (cf. https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookJetEnergyCorrections#CMSSW_7_6_4_and_above )

from  PhysicsTools.PatAlgos.producersLayer1.jetUpdater_cfi import *

# AK4PFchs, AK4PFPuppi, AK8PFchs, AK8PFPuppi

## AK4 Jets
jetCorrFactorsAK4PFchs = patJetCorrFactors.clone(src='slimmedJets',
    levels = cms.vstring(
        'L1FastJet',
        'L2Relative',
        'L3Absolute',
	     'L2L3Residual'),
    payload = cms.string('AK4PFchs'),
    primaryVertices = cms.InputTag("offlineSlimmedPrimaryVertices"),
)

updatedPatJetsAK4PFchs = updatedPatJets.clone(
	addBTagInfo=False,
	jetSource='slimmedJets',
	jetCorrFactorsSource=cms.VInputTag(cms.InputTag("jetCorrFactorsAK4PFchs") ),
)

AK4PFchs = cms.Task()
AK4PFchs.add(jetCorrFactorsAK4PFchs)
AK4PFchs.add(updatedPatJetsAK4PFchs)


## AK8 Jets
jetCorrFactorsAK8PFchs = patJetCorrFactors.clone(src='slimmedJetsAK8',
    levels = cms.vstring(
        'L1FastJet',
        'L2Relative',
        'L3Absolute',
	     'L2L3Residual'),
    payload = cms.string('AK8PFchs'),
    primaryVertices = cms.InputTag("offlineSlimmedPrimaryVertices"),
)

updatedPatJetsAK8PFchs = updatedPatJets.clone(
	addBTagInfo=False,
	jetSource='slimmedJetsAK8',
	jetCorrFactorsSource=cms.VInputTag(cms.InputTag("jetCorrFactorsAK8PFchs") ),
)

AK8PFchs = cms.Task()
AK8PFchs.add(jetCorrFactorsAK8PFchs)
AK8PFchs.add(updatedPatJetsAK8PFchs)


## Puppi Jets

jetCorrFactorsAK4PFPuppi = patJetCorrFactors.clone(src='slimmedJetsPuppi',
    levels = cms.vstring(
        'L1FastJet',
        'L2Relative',
        'L3Absolute',
	     'L2L3Residual'),
    payload = cms.string('AK4PFPuppi'),
    primaryVertices = cms.InputTag("offlineSlimmedPrimaryVertices"),
)


updatedPatJetsAK4PFPuppi = updatedPatJets.clone(
	addBTagInfo=False,
	jetSource='slimmedJetsPuppi',
	jetCorrFactorsSource=cms.VInputTag(cms.InputTag("jetCorrFactorsAK4PFPuppi") ),
)

AK4PFPuppi = cms.Task()
AK4PFPuppi.add(jetCorrFactorsAK4PFPuppi)
AK4PFPuppi.add(updatedPatJetsAK4PFPuppi)


