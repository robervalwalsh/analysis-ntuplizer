# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: step2 --step=L1REPACK:FullSimHcalTP,HLT:User --conditions=90X_upgrade2017_TSG_Hcal_V2 --filein=/store/mc/PhaseIFall16DR/SUSYGluGluToBBHToBB_NarrowWidth_M-300_TuneCUETP8M1_13TeV-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v1/50000/003C6E24-2415-E711-8D09-D067E5F91B8A.root --secondfilein= --custom_conditions= --number=100 --mc --no_exec --datatier RAW --eventcontent=RAW --customise=HLTrigger/Configuration/CustomConfigs.L1THLT --era=Run2_2017 --customise= --scenario=pp --python_filename=ReHLT_L1Trepack_HLTUser_MCNtuple.py --processName=HLT2 --no_output
import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras

process = cms.Process('HLT2',eras.Run2_2017)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.SimL1EmulatorRepack_FullMC_cff')
process.load('HLTrigger.Configuration.HLT_User_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1000)
)

# Input source
process.source = cms.Source("PoolSource",
#    fileNames = cms.untracked.vstring('/store/mc/PhaseIFall16DR/SUSYGluGluToBBHToBB_NarrowWidth_M-300_TuneCUETP8M1_13TeV-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v1/50000/003C6E24-2415-E711-8D09-D067E5F91B8A.root'),
    fileNames = cms.untracked.vstring('/store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130002/364565EB-3812-E711-82A4-0026B937D37D.root'),
    secondaryFileNames = cms.untracked.vstring()
)

process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('step2 nevts:100'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

# Additional output definition

# Other statements
from HLTrigger.Configuration.CustomConfigs import ProcessName
process = ProcessName(process)

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '90X_upgrade2017_TSG_Hcal_V3', '')

# Path and EndPath definitions
process.L1RePack_step = cms.Path(process.SimL1Emulator)
process.endjob_step = cms.EndPath(process.endOfProcess)

#_______________________________________________________________

# include ntuplizer (+ filters) within cmsDriver config
#_______________ Addition to cmsDriver - begin

isMC = True

## Filter counter (maybe more useful for MC)
process.TotalEvents    = cms.EDProducer("EventCountProducer")
process.FilteredEvents = cms.EDProducer("EventCountProducer")

# pileup filter MC
process.RemovePileUpDominatedEventsGen = cms.EDFilter("RemovePileUpDominatedEventsGen",
     generatorInfo = cms.InputTag("generator"),
     pileupSummaryInfos = cms.InputTag("addPileupInfo"),
     )

# Trigger filter (HLT config)
from Analysis.Ntuplizer.TriggerFilter_cfi import triggerFilter

# =========================
# Trigger config modifications
process.triggerFilter = triggerFilter.clone()
process.triggerFilter.hltResults = cms.InputTag( 'TriggerResults', '', 'HLT' )
process.triggerFilter.triggerConditions  = cms.vstring  ('HLT_ZeroBias_v*')
# =========================                                  
# Filtering the trigger sequence                                  
# comment or modified the lines below if no filter or other filters are required
if isMC:
   process.triggerFilter.hltResults = cms.InputTag( 'TriggerResults', '', 'HLT2' )
   process.triggerFilter.triggerConditions  = cms.vstring('HLT_ZeroBias_v*')
   process.HLTBeginSequence.insert(-1,process.RemovePileUpDominatedEventsGen)   # qcd MC
else:
   process.HLTBeginSequence.insert(-1,process.triggerFilter)                    # data
# =========================


# Ntuplizer
from Analysis.Ntuplizer.Ntuplizer_cfi import TFileService
process.TFileService = TFileService.clone()
process.TFileService.fileName = cms.string('/nfs/dust/cms/user/walsh/tmp/ntuple.root')

from Analysis.Ntuplizer.Ntuplizer_cfi import ntuplizer
process.MssmHbbTrigger = ntuplizer.clone()
process.MssmHbbTrigger.MonteCarlo        = cms.bool(isMC)
process.MssmHbbTrigger.TotalEvents       = cms.InputTag("TotalEvents")
process.MssmHbbTrigger.FilteredEvents    = cms.InputTag("FilteredEvents")
process.MssmHbbTrigger.L1TJets           = cms.VInputTag(cms.InputTag('hltGtStage2Digis','Jet'))
process.MssmHbbTrigger.L1TMuons          = cms.VInputTag(cms.InputTag('hltGtStage2Digis','Muon'))
# # For trigger info see Analysis.Ntuplizer.Ntuplizer_cfi
process.MssmHbbTrigger.TriggerResults    = cms.VInputTag(cms.InputTag('TriggerResults','','HLT2'))
process.MssmHbbTrigger.TriggerPaths      = cms.vstring (
                                   'HLT_ZeroBias_v',
                                   'HLT_Mu12_v',
                                   'HLT_DoublePFJets40_v',
                                   'HLT_DoublePFJets100_v',
                                   'HLT_BTagMu_DiJet20_Mu5_v',
                                   'HLT_DoubleJets30_Mu12_SingleBTagCSV_0p92_DoublePFJets40_v',
                                   'HLT_DoubleJets30_Mu12_SingleBTagCSV_0p92_DoublePFJets100_v',
                                   'HLT_DoubleJets30_Mu12_SingleBTagCSV_0p92_DoublePFJets200_v',
                                   'HLT_DoubleJets30_Mu12_SingleBTagCSV_0p92_DoublePFJets350_v',
                                   'HLT_DoubleJets30_Mu12_DoubleBTagCSV_0p92_DoublePFJets40MaxDeta1p6_v',
                                   'HLT_DoubleJets30_Mu12_DoubleBTagCSV_0p92_DoublePFJets54MaxDeta1p6_v',
                                   'HLT_DoubleJets30_Mu12_DoubleBTagCSV_0p92_DoublePFJets62MaxDeta1p6_v',
                                   'HLT_DoubleJets30_SingleBTagCSV_0p92_DoublePFJets40_v',
                                   'HLT_DoubleJets100_SingleBTagCSV_0p92_DoublePFJets100_v',
                                   'HLT_DoubleJets100_SingleBTagCSV_0p92_DoublePFJets200_v',
                                   'HLT_DoubleJets100_SingleBTagCSV_0p92_DoublePFJets350_v',
                                   'HLT_DoubleJets100_DoubleBTagCSV_0p92_DoublePFJets100MaxDeta1p6_v',
                                   'HLT_DoubleJets100_DoubleBTagCSV_0p92_DoublePFJets116MaxDeta1p6_v',
                                   'HLT_DoubleJets100_DoubleBTagCSV_0p92_DoublePFJets128MaxDeta1p6_v',
                                   )
process.MssmHbbTrigger.TriggerObjectLabels    = cms.vstring  (
                                   'hltBDiJet20L1FastJetCentral',
                                   'hltBSoftMuonDiJet20L1FastJetL25FilterByDR',
                                   'hltBSoftMuonDiJet20L1FastJetMu5L3FilterByDR',
                                   'hltBSoftMuonDijet100Mu12L3FilterByDR',
                                   'hltBSoftMuonDijet40Mu12L3FilterByDR',
                                   'hltBSoftMuonDijet54Mu12L3FilterByDR',
                                   'hltBSoftMuonDijet62Mu12L3FilterByDR',
                                   'hltBTagCalo30x8CSVp0p92DoubleWithMatching',
                                   'hltBTagCalo30x8CSVp0p92SingleWithMatching',
                                   'hltBTagCalo80x6CSVp0p92DoubleWithMatching',
                                   'hltBTagCalo80x6CSVp0p92SingleWithMatching',
                                   'hltDoubleCaloBJets100eta2p3',
                                   'hltDoubleCaloBJets30eta2p3',
                                   'hltDoubleCaloJets30eta2p3',
                                   'hltDoublePFBJets100Eta2p3',
                                   'hltDoublePFBJets40Eta2p3',
                                   'hltDoublePFBJets54Eta2p3',
                                   'hltDoublePFBJets62Eta2p3',
                                   'hltDoublePFJets100Eta2p3',
                                   'hltDoublePFJets100Eta2p3MaxDeta1p6',
                                   'hltDoublePFJets116Eta2p3',
                                   'hltDoublePFJets116Eta2p3MaxDeta1p6',
                                   'hltDoublePFJets128Eta2p3',
                                   'hltDoublePFJets128Eta2p3MaxDeta1p6',
                                   'hltDoublePFJets200Eta2p3',
                                   'hltDoublePFJets350Eta2p3',
                                   'hltDoublePFJets40Eta2p3',
                                   'hltDoublePFJets40Eta2p3MaxDeta1p6',
                                   'hltDoublePFJets54Eta2p3MaxDeta1p6',
                                   'hltDoublePFJets62Eta2p3MaxDeta1p6',
                                   'hltL1DoubleJet100er2p3dEtaMax1p6',
                                   'hltL1DoubleJet100er3p0',
                                   'hltL1DoubleJet112er3p0',
                                   'hltL1DoubleJet40er3p0',
                                   'hltL1Mu12er2p3Jet40er2p3dRMax0p4DoubleJet40er2p3dEtaMax1p6',
                                   'hltL1fL1sMu12Dijet40L1Filtered0',
                                   'hltL1fL1sMu3Jet16L1Filtered0',
                                   'hltL1fL1sMu3Jet60L1Filtered0',
                                   'hltL1fL1sMu7L1Filtered12',
                                   'hltL1sMu3JetC120dEtaMax0p4dPhiMax0p4',
                                   'hltL1sMu3JetC16dEtaMax0p4dPhiMax0p4',
                                   'hltL1sMu3JetC60dEtaMax0p4dPhiMax0p4',
                                   'hltL1sSingleMu7',
                                   'hltL1sZeroBias',
                                   'hltL2fL1sMu12Dijet40L1f0L2Filtered8',
                                   'hltL2fL1sMu3Jet16L1f0L2Filtered8',
                                   'hltL2fL1sMu3Jet60L1f0L2Filtered8',
                                   'hltL2fL1sMu7L1f12L2Filtered8',
                                   'hltL3fL1sMu12Dijet40L1f0L2f8L3Filtered12',
                                   'hltL3fL1sMu3Jet16L1f0L2f8L3Filtered12',
                                   'hltL3fL1sMu3Jet60L1f0L2f8L3Filtered12',
                                   'hltL3fL1sMu5L1f12L2f8L3Filtered12',
                                   )


if isMC:
   # MC specific
   process.MssmHbbTrigger.PileupInfo        = cms.InputTag("addPileupInfo","","HLT")
   process.MssmHbbTrigger.GenFilterInfo     = cms.InputTag("genFilterEfficiencyProducer")
   process.MssmHbbTrigger.GenRunInfo        = cms.InputTag("generator")

process.Ntuplizer = cms.Sequence( process.TotalEvents + process.triggerFilter  + process.FilteredEvents + process.MssmHbbTrigger)
   
process.ntuplizer_step = cms.EndPath(process.Ntuplizer)

#_______________ Addition to cmsDriver - end


# Schedule definition
process.schedule = cms.Schedule(process.L1RePack_step)
process.schedule.extend(process.HLTSchedule)
process.schedule.extend([process.endjob_step,process.ntuplizer_step]) # Modified wrt cmsDriver 
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)

# customisation of the process.

# Automatic addition of the customisation function from HLTrigger.Configuration.CustomConfigs
from HLTrigger.Configuration.CustomConfigs import L1THLT 

#call to customisation function L1THLT imported from HLTrigger.Configuration.CustomConfigs
process = L1THLT(process)

# Automatic addition of the customisation function from HLTrigger.Configuration.customizeHLTforMC
from HLTrigger.Configuration.customizeHLTforMC import customizeHLTforMC 

#call to customisation function customizeHLTforMC imported from HLTrigger.Configuration.customizeHLTforMC
process = customizeHLTforMC(process)

# End of customisation functions

# Customisation from command line

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
